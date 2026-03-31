export interface EmojiCategory {
  name: string
  emojis: { icon: string; label: string }[]
}

export const emojiCategories: EmojiCategory[] = [
  {
    name: '电子产品',
    emojis: [
      { icon: '📱', label: '手机' }, { icon: '📲', label: '来电' }, { icon: '💻', label: '笔记本' }, { icon: '🖥️', label: '台式机' },
      { icon: '⌨️', label: '键盘' }, { icon: '🖱️', label: '鼠标' }, { icon: '🖲️', label: '轨迹球' },
      { icon: '🎧', label: '耳机' }, { icon: '🔊', label: '音箱' }, { icon: '🎤', label: '麦克风' }, { icon: '📻', label: '收音机' },
      { icon: '📺', label: '电视' }, { icon: '📡', label: '卫星天线' },
      { icon: '📹', label: '摄像机' }, { icon: '🎥', label: '电影摄影' }, { icon: '📸', label: '相机' }, { icon: '📷', label: '拍立得' },
      { icon: '📟', label: '传呼机' }, { icon: '📠', label: '传真机' }, { icon: '🔌', label: '插头' },
      { icon: '🔋', label: '电池' }, { icon: '⏱️', label: '秒表' }, { icon: '⏲️', label: '定时器' },
      { icon: '⏰', label: '闹钟' }, { icon: '⌚', label: '手表' }, { icon: '📞', label: '电话' }, { icon: '🖨️', label: '打印机' },
      { icon: '💽', label: '光盘' }, { icon: '💾', label: '软盘' }, { icon: '💿', label: 'CD' }, { icon: '📀', label: 'DVD' },
      { icon: '📼', label: '录像带' }, { icon: '🎙️', label: '录音' }, { icon: '📺', label: '显示器' }
    ]
  },
  {
    name: '家用电器',
    emojis: [
      { icon: '❄️', label: '空调' }, { icon: '🌡️', label: '温度计' }, { icon: '🌬️', label: '风扇' }, { icon: '💡', label: '灯泡' }, { icon: '🔦', label: '手电筒' },
      { icon: '🧹', label: '扫帚' }, { icon: '🧺', label: '洗衣篮' }, { icon: '🧻', label: '纸巾' }, { icon: '🪣', label: '水桶' }, { icon: '🧼', label: '肥皂' },
      { icon: '🧯', label: '灭火器' }, { icon: '🔑', label: '钥匙' }, { icon: '🔒', label: '锁' }, { icon: '🪟', label: '窗户' },
      { icon: '🚪', label: '门' }, { icon: '🪑', label: '椅子' }, { icon: '🛋️', label: '沙发' }, { icon: '🛏️', label: '床' }, { icon: '🧸', label: '玩偶' },
      { icon: '🖼️', label: '画框' }, { icon: '🪞', label: '镜子' }, { icon: '🪜', label: '梯子' }, { icon: '🧳', label: '行李箱' }
    ]
  },
  {
    name: '生活用品',
    emojis: [
      { icon: '🪥', label: '牙刷' }, { icon: '🧴', label: '乳液' }, { icon: '🧽', label: '海绵' },
      { icon: '💊', label: '药品' }, { icon: '🩹', label: '创可贴' }, { icon: '🩺', label: '听诊器' }, { icon: '🪒', label: '剃刀' },
      { icon: '☂️', label: '雨伞' }, { icon: '🧣', label: '围巾' }, { icon: '🧤', label: '手套' }, { icon: '🧦', label: '袜子' },
      { icon: '💍', label: '戒指' }, { icon: '💎', label: '宝石' }, { icon: '🛍️', label: '购物袋' },
      { icon: '🪡', label: '针线' }, { icon: '🧵', label: '线团' }, { icon: '🛁', label: '浴缸' }
    ]
  },
  {
    name: '服饰鞋包',
    emojis: [
      { icon: '👕', label: 'T恤' }, { icon: '👖', label: '牛仔裤' }, { icon: '👗', label: '连衣裙' }, { icon: '👘', label: '和服' }, { icon: '🥻', label: '纱丽' },
      { icon: '👙', label: '比基尼' }, { icon: '👚', label: '衬衫' },
      { icon: '👛', label: '钱包' }, { icon: '👜', label: '手提包' }, { icon: '👝', label: '手拿包' }, { icon: '🎒', label: '背包' },
      { icon: '👞', label: '皮鞋' }, { icon: '👟', label: '运动鞋' }, { icon: '🥾', label: '靴子' }, { icon: '👠', label: '高跟鞋' }, { icon: '👢', label: '长靴' },
      { icon: '👑', label: '皇冠' }, { icon: '🎓', label: '学士帽' }, { icon: '🧢', label: '鸭舌帽' }, { icon: '🧣', label: '围巾' }
    ]
  },
  {
    name: '运动健康',
    emojis: [
      { icon: '⚽', label: '足球' }, { icon: '🏀', label: '篮球' }, { icon: '🏈', label: '橄榄球' }, { icon: '⚾', label: '棒球' }, { icon: '🎾', label: '网球' },
      { icon: '🏐', label: '排球' }, { icon: '🏓', label: '乒乓球' }, { icon: '🏸', label: '羽毛球' }, { icon: '🏒', label: '冰球' },
      { icon: '🎯', label: '飞镖' }, { icon: '🏹', label: '射箭' }, { icon: '🎣', label: '钓鱼' }, { icon: '🥊', label: '拳击' }, { icon: '🥋', label: '柔道' },
      { icon: '🎽', label: '运动服' }, { icon: '🛹', label: '滑板' }, { icon: '🛷', label: '雪橇' }, { icon: '⛷️', label: '滑雪' }, { icon: '🏂', label: '单板' },
      { icon: '🏋️', label: '举重' }, { icon: '🤼', label: '摔跤' }
    ]
  },
  {
    name: '休闲娱乐',
    emojis: [
      { icon: '🎲', label: '骰子' }, { icon: '🎴', label: '花牌' }, { icon: '🎵', label: '音符' }, { icon: '🎶', label: '音乐' }, { icon: '🎸', label: '吉他' },
      { icon: '🎹', label: '钢琴' }, { icon: '🥁', label: '鼓' }, { icon: '🎷', label: '萨克斯' }, { icon: '🎺', label: '喇叭' }, { icon: '🎻', label: '小提琴' },
      { icon: '🎬', label: '电影' }, { icon: '🎭', label: '戏剧' }, { icon: '🎨', label: '调色板' }, { icon: '🧩', label: '拼图' },
      { icon: '🕹️', label: '游戏机' }, { icon: '🎮', label: '手柄' }, { icon: '🎪', label: '马戏' }, { icon: '🧸', label: '玩偶' }
    ]
  },
  {
    name: '学习办公',
    emojis: [
      { icon: '📚', label: '书本' }, { icon: '📖', label: '打开的书' }, { icon: '📕', label: '红色书' }, { icon: '📗', label: '绿色书' }, { icon: '📘', label: '蓝色书' },
      { icon: '📓', label: '笔记本' }, { icon: '📝', label: '备忘录' }, { icon: '💼', label: '公文包' }, { icon: '📁', label: '文件夹' }, { icon: '📂', label: '打开文件夹' },
      { icon: '🗓️', label: '日历' }, { icon: '📋', label: '剪贴板' }, { icon: '📌', label: '图钉' }, { icon: '✏️', label: '铅笔' }, { icon: '🖊️', label: '钢笔' },
      { icon: '🖨️', label: '打印机' }, { icon: '📎', label: '回形针' }, { icon: '📏', label: '直尺' }
    ]
  },
  {
    name: '软件服务',
    emojis: [
      { icon: '🌐', label: '全球网' }, { icon: '☁️', label: '云' }, { icon: '📊', label: '图表' }, { icon: '📈', label: '上升趋势' }, { icon: '📉', label: '下降趋势' },
      { icon: '⚙️', label: '设置' }, { icon: '🔧', label: '扳手' }, { icon: '🛠️', label: '工具' }, { icon: '🔗', label: '链接' }, { icon: '🔒', label: '安全' },
      { icon: '🤖', label: '机器人' }, { icon: '💬', label: '聊天' }, { icon: '🧬', label: 'DNA' }, { icon: '🔭', label: '望远镜' }, { icon: '🔬', label: '显微镜' }
    ]
  },
  {
    name: '其他',
    emojis: [
      { icon: '📦', label: '包裹' }, { icon: '🎁', label: '礼物' }, { icon: '🎈', label: '气球' }, { icon: '🎉', label: '派对' },
      { icon: '🏡', label: '房子' }, { icon: '🏢', label: '办公楼' }, { icon: '🏥', label: '医院' }, { icon: '🏦', label: '银行' },
      { icon: '🏫', label: '学校' }, { icon: '🏭', label: '工厂' }, { icon: '🏰', label: '城堡' }, { icon: '🗼', label: '东京塔' },
      { icon: '🗽', label: '自由女神' }, { icon: '🏞️', label: '公园' }, { icon: '🌅', label: '日出' }, { icon: '🌆', label: '黄昏' },
      { icon: '🌃', label: '夜景' }, { icon: '🌌', label: '星空' }, { icon: '🌉', label: '夜景桥' }
    ]
  }
]
