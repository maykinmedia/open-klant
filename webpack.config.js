const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const argv = require('yargs').argv;

module.exports = {
    // No entry at all if you only want to compile CSS from JS imports.
    entry: {},

    output: {
        path: path.resolve(__dirname, 'static/bundles'), // adjust to your jsDir
        filename: '[name].js', // only generates files for real entries
    },

    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css', // only extracts CSS from actual JS imports
        }),
    ],

    module: {
        rules: [
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    { loader: 'css-loader', options: { url: false } },
                    { loader: 'postcss-loader' },
                    {
                        loader: 'sass-loader',
                        options: {
                            sassOptions: { comments: false, style: 'compressed' },
                            sourceMap: argv.sourcemap,
                        },
                    },
                ],
            },
        ],
    },

    mode: process.env.NODE_ENV === 'production' || argv.production ? 'production' : 'development',
    devtool: argv.sourcemap ? 'sourcemap' : false,
};
