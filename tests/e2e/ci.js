exports.config = require('./config.js').config;

exports.config.sauceUser = process.env.SAUCE_USER;
exports.config.sauceKey = process.env.SAUCE_KEY;

var multiCapabilities = [];

multiCapabilities.push({
    browserName: 'firefox',
    version: '37.0',
    platform: 'Windows 7'
});

multiCapabilities.push({
    browserName: 'chrome',
    version: '39.0',
    platform: 'Windows 7'
});

multiCapabilities.forEach(function (item) {
    item.name = 'End-to-End' || 'local Integration';
    item.build = process.env.VERSION || 'local';
    item.count = 1;
});

exports.config.multiCapabilities = multiCapabilities;