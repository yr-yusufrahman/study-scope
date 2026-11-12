/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html", 
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          "primary": "#2a9bb5",
          "primary-content": "#ffffff",
          "secondary": "#1d6d84",
          "secondary-content": "#ffffff",
          "accent": "#3e7c8f",
          "accent-content": "#ffffff",
          "neutral": "#243044",
          "neutral-content": "#f6f8fc",
          "base-100": "#ffffff",
          "base-200": "#f3f7fb",
          "base-300": "#e4edf4",
          "base-content": "#243044",
          "info": "#3aa0c4",
          "info-content": "#ffffff",
          "success": "#2f8f72",
          "success-content": "#ffffff",
          "warning": "#c4842a",
          "warning-content": "#ffffff",
          "error": "#c45555",
          "error-content": "#ffffff",
        },
      },
    ],
  },
}

