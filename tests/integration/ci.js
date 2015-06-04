exports.config = require('./config.js').config;

exports.config.sauceUser = process.env.SAUCE_USER;
exports.config.sauceKey = process.env.SAUCE_KEY;
exports.config.sauceSeleniumAddress = 'localhost:4445/wd/hub';

exports.config.capabilities = {
    browserName: 'firefox',
    version: '32.0',
    platform: 'Windows 7',
    name: 'Integration' || 'local Integration',
    build: process.env.VERSION,
    count: 1
};
