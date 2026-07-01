/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Background colors
        background: {
          primary: '#080D1A',
          secondary: '#0D1528',
          hover: '#111E35',
        },
        // Border colors
        border: {
          DEFAULT: '#1E2D4A',
        },
        // Accent colors
        accent: {
          blue: '#3B7BF6',
          amd: '#ED1C24',
        },
        // Text colors
        text: {
          primary: '#F0F4FF',
          secondary: '#8B9CC8',
        },
        // Semantic colors
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      screens: {
        sm: '375px',
        md: '768px',
        lg: '1024px',
        xl: '1280px',
        '2xl': '1536px',
      },
    },
  },
  plugins: [],
};
