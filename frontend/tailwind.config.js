/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#0b0f19",
          card: "#111827",
          hover: "#1f2937",
          border: "#1e293b",
        },
        brand: {
          blue: "#3b82f6",
          purple: "#8b5cf6",
          indigo: "#6366f1",
          emerald: "#10b981",
          amber: "#f59e0b",
          rose: "#f43f5e"
        }
      }
    },
  },
  plugins: [],
}
