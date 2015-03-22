var path = require('path');
var StatsWriterPlugin = require('webpack-stats-plugin').StatsWriterPlugin;


module.exports = {
    entry: {
        server: './assets/js/server.js',
        client: './assets/js/client.jsx'
    },
    output: {
        filename: '[name]-[chunkhash].js',
        publicPath: 'http://localhost:8090/static',
        path: 'tornado_react_demo/static/js',
        libraryTarget: 'this'
    },
    module: {
        loaders: [
            {
                test: /\.jsx$/,
                loader: 'jsx-loader?harmony'
            }
        ]
    },
    externals: {
        //don't bundle the 'react' npm package with our bundle.js
        //but get it from a global 'React' variable
        //'react': 'React'
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    plugins: [
        new StatsWriterPlugin({
            path: path.join(__dirname, 'tornado_react_demo', 'data'),
            filename: 'manifest.json'
        })
    ]
};
