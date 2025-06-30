/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // YNA Brand Colors
        primary: {
          50: '#e6eafe',
          100: '#ccd5fd',
          200: '#99abfa',
          300: '#6681f8',
          400: '#3357f5',
          500: '#1A2A72', // Deep Blue - Main brand color
          600: '#15225c',
          700: '#101b47',
          800: '#0b1431',
          900: '#060d1c',
          950: '#030608',
        },
        accent: {
          50: '#fef9e6',
          100: '#fef3cc',
          200: '#fde799',
          300: '#fcdb66',
          400: '#fbcf33',
          500: '#FBB03B', // Accent Yellow/Orange - Main accent color
          600: '#c98d2f',
          700: '#976a23',
          800: '#644617',
          900: '#32230c',
          950: '#191106',
        },
        navy: {
          50: '#e3e7f4',
          100: '#c7cfe9',
          200: '#8f9fd3',
          300: '#576fbd',
          400: '#1f3fa7',
          500: '#081C45', // Navy - Dark brand color
          600: '#061637',
          700: '#051129',
          800: '#030b1c',
          900: '#02060e',
          950: '#010307',
        },
        // Semantic colors
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        arabic: ['Noto Sans Arabic', 'Cairo', 'system-ui', 'sans-serif'],
        display: ['Poppins', 'system-ui', 'sans-serif'],
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
        "fade-in": "fade-in 0.5s ease-in-out",
        "slide-in": "slide-in 0.3s ease-out",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        "slide-in": {
          from: { transform: "translateY(20px)", opacity: "0" },
          to: { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}