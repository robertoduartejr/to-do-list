const path = require('path');

module.exports = {
    mode: 'development',

    entry: "./frontend/index.js",

    output: {
        path: path.resolve(__dirname, '../static/js'),
        filename: 'index.bundle.js'
    },

    resolve: {
        extensions: ['.js', '.jsx']
    },

    module: {
        rules: [
            { test: /\.js[x]?$/, use: 'babel-loader' },
             { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] }
        ]
    }
}