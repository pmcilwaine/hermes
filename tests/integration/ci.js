exports.config = require('./config.js').config;

exports.config.sauceUser = process.env.SAUCE_USER;
exports.config.sauceKey = process.env.SAUCE_KEY;
exports.config.sauceSeleniumAddress = 'localhost:4445/wd/hub';

exports.config.capabilities = {
    browserName: 'chrome',
    version: '41.0',
    name: process.env.VERSION || 'local',
    count: 1
};
