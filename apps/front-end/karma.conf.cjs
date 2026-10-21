const path = require('node:path');

module.exports = function configureKarma(config) {
  config.set({
    frameworks: ['jasmine'],

    plugins: [
      require('karma-jasmine'),
      require('karma-chrome-launcher'),
      require('karma-jasmine-html-reporter'),
      require('karma-coverage'),
    ],

    browsers: ['Chrome'],
    singleRun: true,

    reporters: ['progress', 'kjhtml'],

    coverageReporter: {
      dir: path.join(__dirname, 'coverage/ng-sonar'),
      subdir: '.',
      reporters: [
        { type: 'html' },
        { type: 'text-summary' },
        { type: 'lcovonly', file: 'lcov.info' },
      ],
    },
  });
};
