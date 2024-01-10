const paths = require('./build/paths');
const webpackConfig = require('./webpack.config.js');

// Prevent testing infrastructure from crashing (MIGHT REQUIRE --production --sourcemap NOT TO BE SET!
webpackConfig.output.library = undefined;


// The preprocessor config
const preprocessors = {};
preprocessors[paths.jsSpecEntry] = [
    'webpack'
];


// The main configuration
const configuration = function (config) {
    config.set({
        frameworks: [
            'mocha'
        ],

        files: [
            'node_modules/@babel/polyfill/dist/polyfill.js',
            paths.jsSpecEntry
        ],

        singleRun: true,
        preprocessors: preprocessors,

        webpack: webpackConfig,

        webpackMiddleware: {
            noInfo: true
        },

        reporters: ['coverage', 'junit', 'spec'],

        coverageReporter: {
            dir: 'reports/jstests/',
            reporters: [
                {type: 'html'},
                {type: 'text'},
                {type: 'text-summary'},
            ]
        },

        junitReporter: {
          outputDir: 'reports/jstests/',
          outputFile: 'junit.xml',
          useBrowserName: false,
        },

        browsers: ['Chromium'],
    });
};

module.exports = configuration;
