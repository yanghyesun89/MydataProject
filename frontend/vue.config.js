const { defineConfig } = require("@vue/cli-service");

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/chat": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
