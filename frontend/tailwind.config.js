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
      colors: {
        primary: {
          DEFAULT: '#6366F1',
          dark: '#764BA2',
          light: '#818CF8',
        }
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
