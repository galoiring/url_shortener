const path = require("path");

module.exports = {
  entry: "./shortener/static/shortener/js/index.js",
  output: {
    path: path.resolve(__dirname, "shortener/static/shortener/js/dist"),
    filename: "bundle.js",
    publicPath: "/static/shortener/js/dist/",
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-react"],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader", "postcss-loader"],
      },
    ],
  },
  resolve: {
    extensions: [".js", ".jsx"],
  },
  mode: "development",
};
