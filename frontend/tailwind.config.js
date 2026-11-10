/** @type {import('tailwindcss').Config} */
// Old-library system: aged parchment surfaces, walnut ink, leather dark
// section, brass accents. Flat colors only — texture comes from the subtle
// repeating stone-wall pattern defined in index.css.
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F4EDDF",   // aged parchment — main background
        vellum: "#ECE1CC",  // deeper parchment — alt background
        ink: "#2B2117",     // dark walnut — text & primary buttons
        leather: "#231911", // near-black brown — dark section & footer
        line: "#D8CBB0",    // hairline borders / empty stars
        fade: "#77694F",    // secondary text
        brass: "#8B6B43",   // quiet accent
        "brass-light": "#C9A876", // accent readable on dark leather
      },
      fontFamily: {
        display: ['"Playfair Display"', "Georgia", "serif"],
        sans: ['"Inter"', "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
