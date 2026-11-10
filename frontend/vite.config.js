import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // In containerized dev, talk to the backend by name
    proxy: {
      "/api": "http://backend:8000",
    },
  },
});
