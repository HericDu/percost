/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['PingFang SC', 'SF Pro Display', '-apple-system', 'Microsoft YaHei', 'sans-serif'],
      },
      // Apple 式圆角：半径随元素体量等比放大，保持「圆润连续」的同一曲率感受。
      // 同层级元素必须用同一档 —— Dock 与卡片同为「内容面板」，共用 card。
      borderRadius: {
        'ctl-sm': '10px',   // 图标小按钮
        'ctl': '14px',      // 常规按钮
        'pill': '999px',    // 输入框、分页、胶囊控件
        'card': '22px',     // 卡片、顶部 Dock、空状态面板
        'modal': '28px',    // 弹窗（唯一更高一档）
      },
      colors: {
        primary: {
          DEFAULT: '#6366F1',
          dark: '#764BA2',
          light: '#818CF8',
        },
        // 中性色向品牌靛蓝微偏，避免纯灰的机械感
        ink: {
          900: '#1a1a2e',
          800: '#2d2d44',
          700: '#45455c',
          600: '#5c5c75',
          500: '#78788f',
          400: '#9a9ab0',
          300: '#bcbcce',
          200: '#d8d8e4',
          100: '#ebebf3',
        },
      },
      animation: {
        'fadeIn': 'fadeIn 0.3s ease-in-out',
        'bounce-gentle': 'bounce-gentle 2s infinite',
        'float': 'float 3s ease-in-out infinite',
        'shine': 'shine 0.6s ease-out',
        'press': 'press 0.15s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'bounce-gentle': {
          '0%, 100%': { transform: 'translateY(-5%)' },
          '50%': { transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        shine: {
          '0%': { left: '-100%' },
          '100%': { left: '100%' },
        },
        press: {
          '0%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(0.97)', filter: 'brightness(0.95)' },
          '100%': { transform: 'scale(1)', filter: 'brightness(1)' },
        },
      }
    },
  },
  plugins: [],
}
