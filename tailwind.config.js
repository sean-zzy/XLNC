/** @type {import('tailwindcss').Config} */
export default {
  content: ["./xlnc/routes/**/*.{html,js}", "node_modules/preline/dist/*.js"],
  theme: {
    extend: {},
  },
  plugins: [require("preline/plugin")],
};
