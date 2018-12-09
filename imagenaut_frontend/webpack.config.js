const path = require('path');

module.exports = {
  mode: 'production',
  target: 'node',
  entry: './src/index.jsx',
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      "react": path.resolve(__dirname, './node_modules/react'),
      "react-dom": path.resolve(__dirname, './node_modules/react-dom')
    }
  },
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: path.resolve(__dirname, './node_modules/'),
        use: ["babel-loader", "eslint-loader"]
      }
    ]
  },
};
