var path = require('path');
var webpack = require('webpack');

// Third party plugins
var ManifestRevisionPlugin = require('manifest-revision-webpack-plugin');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

// Development asset host, asset location and build output path.
var publicHost = 'http://localhost:2992';
var rootAssetPath = path.join(__dirname, 'eGrader/static');
var cssAssetPath = path.join(__dirname, 'eGrader/static/css');
var buildOutputPath = path.join(__dirname, 'eGrader/static/build/');

module.exports = {
    context: path.join(__dirname, 'eGrader'),
    entry: {
        app_js: [
            // 'webpack/hot/dev-server',
            rootAssetPath + '/js/app/main'
        ],
        app_css: [
            cssAssetPath + '/style',
            cssAssetPath + '/dashboard'
        ]
    },
    output: {
        path: buildOutputPath,
        publicPath: publicHost + '/static/',
        filename: '[name].[hash].js',
        chunkFilename: '[id].[chunkhash].js'
    },
    resolve: {
        extensions: ['', '.js', '.jsx', '.css']
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                loader: 'babel',
                query: {
                    presets: ['es2015']
                }
            },
            {
                test: /\.css$/i,
                loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
            },
            {
                test: /\.(jpe?g|png|gif|svg([\?]?.*))$/i,
                loaders: [
                    'file?context=' + rootAssetPath + '&name=[path][name].[hash].[ext]',
                    'image?bypassOnDebug&optimizationLevel=7&interlaced=false'
                ]
            }
        ]
    },
    plugins: [
        new ManifestRevisionPlugin(rootAssetPath + '/manifest.json', {
            rootAssetPath: rootAssetPath,
            ignorePaths: ['/css', '/js']
        }),
        new ExtractTextPlugin('[name].[chunkhash].css')
    ]
};
