import react from "@vitejs/plugin-react";
import { resolve } from "path";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
  server: {
    port: 9100,
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://localhost:9000",
        changeOrigin: true,
      },
    },
  },
});
