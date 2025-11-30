/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      spacing: {
        '70': '17.5rem', // 280px for sidebar width
      },
      colors: {
        primary: {
          50: '#E8F5E8',
          100: '#C3E6C3',
          200: '#9DD69D',
          300: '#77C677',
          400: '#51B651',
          500: '#0A8A4D',
          600: '#087A44',
          700: '#066A3B',
          800: '#045A32',
          900: '#024A29',
          light: '#1BB673',
          DEFAULT: '#0A8A4D',
          dark: '#065A35',
        },
        emerald: {
          50: '#E8F5E8',
          100: '#C3E6C3',
          200: '#9DD69D',
          300: '#77C677',
          400: '#51B651',
          500: '#0A8A4D',
          600: '#087A44',
          700: '#066A3B',
          800: '#045A32',
          900: '#024A29',
        },
        neutral: {
          50: '#F8FAFC',
          100: '#F1F5F9',
          200: '#E2E8F0',
          300: '#CBD5E1',
          400: '#94A3B8',
          500: '#64748B',
          600: '#475569',
          700: '#334155',
          800: '#1E293B',
          900: '#0F172A',
        },
        secondary: {
          light: '#1BB673',
          DEFAULT: '#0A8A4D',
          dark: '#065A35',
        },
        accent: {
          light: '#1BB673',
          DEFAULT: '#0A8A4D',
          dark: '#065A35',
        },
        surface: {
          DEFAULT: '#262A3B',
          light: '#2F3350',
          dark: '#1E2233',
        },
        mood: {
          happy: '#FFD97D',
          sad: '#7DB9FF',
          chill: '#A48CFF',
          energetic: '#FF8D7D',
          romantic: '#FE79C6',
          focus: '#5CF4E8',
        }
      },
      boxShadow: {
        'glow': '0 0 24px rgba(10, 138, 77, 0.3), 0 0 48px rgba(10, 138, 77, 0.2)',
        'glow-lg': '0 0 40px rgba(10, 138, 77, 0.4), 0 0 80px rgba(10, 138, 77, 0.3)',
        'glow-emerald': '0 0 24px rgba(16, 185, 129, 0.3), 0 0 48px rgba(16, 185, 129, 0.2)',
        'card': '0 4px 20px rgba(0, 0, 0, 0.08)',
        'card-hover': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'brand': '0 10px 15px -3px rgba(10, 138, 77, 0.1), 0 4px 6px -2px rgba(10, 138, 77, 0.05)',
        'brand-lg': '0 20px 25px -5px rgba(10, 138, 77, 0.1), 0 10px 10px -5px rgba(10, 138, 77, 0.04)',
        'soft': '0 4px 16px rgba(0, 0, 0, 0.1)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        glow: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        }
      }
    },
  },
  plugins: [],
}
