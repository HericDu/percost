"""轻量级内存限流。

适用于单进程部署（gunicorn --workers 1）。若将来扩到多 worker 或多实例，
需换成 Redis 等共享存储，否则各进程计数相互独立，限流会被绕过。
"""

import threading
import time

_lock = threading.Lock()
# key -> (失败次数, 窗口起始时间戳)
_buckets: dict[str, tuple[int, float]] = {}

# 条目上限，防止被海量伪造 IP 撑爆内存
_MAX_ENTRIES = 4096


def client_ip(request) -> str:
    """取客户端 IP。

    仅在明确部署于可信反向代理之后时才采信 X-Forwarded-For —— 该头可被伪造，
    直接暴露在公网时应以 remote_addr 为准。
    """
    forwarded = request.headers.get('X-Forwarded-For', '')
    if forwarded:
        # 取最左侧（最接近真实客户端的一跳）
        return forwarded.split(',')[0].strip()
    return request.remote_addr or 'unknown'


def _prune(now: float) -> None:
    """清掉已过期的条目。调用方需持有锁。"""
    expired = [k for k, (_, start) in _buckets.items() if now - start > 3600]
    for k in expired:
        _buckets.pop(k, None)

    # 仍然超限时，丢弃最早的一批
    if len(_buckets) > _MAX_ENTRIES:
        oldest = sorted(_buckets.items(), key=lambda kv: kv[1][1])
        for k, _ in oldest[: len(_buckets) - _MAX_ENTRIES]:
            _buckets.pop(k, None)


def check_rate_limit(key: str, limit: int, window: int) -> tuple[bool, int]:
    """记录一次尝试并判断是否超限。

    返回 (是否允许, 距离窗口结束的剩余秒数)。
    """
    now = time.time()

    with _lock:
        _prune(now)

        count, start = _buckets.get(key, (0, now))

        # 窗口已过期则重新开始计数
        if now - start > window:
            count, start = 0, now

        if count >= limit:
            return False, max(1, int(window - (now - start)))

        _buckets[key] = (count + 1, start)
        return True, 0


def reset_rate_limit(key: str) -> None:
    """操作成功后清除计数，避免正常用户被历史失败拖累。"""
    with _lock:
        _buckets.pop(key, None)
