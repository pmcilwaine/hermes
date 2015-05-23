var chai = require('chai');
chai.use(require('chai-as-promised'));

var expect = chai.expect;
var helpers = {};

helpers.waitUntilDisplayed = function(selector, index, timeout) {

    index = index || 0
    timeout = timeout || 1000

    browser.driver.wait(function () {
        return element.all(selector).get(index).isDisplayed()
    }, timeout)

    return element.all(selector).get(index)
};

helpers.selectDropdown = function(elem, value) {
    elem.all(by.cssContainingText('option', value)).get(0).click();
};

module.exports = helpers;
