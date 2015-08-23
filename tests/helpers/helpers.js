var chai = require('chai');
chai.use(require('chai-as-promised'));

var expect = chai.expect;
var helpers = {};

helpers.waitUntilDisplayed = function(selector, index, timeout) {

    index = index || 0;
    timeout = timeout || 1000;

    browser.driver.wait(function () {
        return element.all(selector).get(index).isDisplayed();
    }, timeout);

    return element.all(selector).get(index);
};

helpers.waitForUrl = function(match, timeout) {
    timeout = timeout || 30000;

    browser.driver.wait(function () {
        return browser.getLocationAbsUrl().then(function (url) {
            return url.match(match);
        });
    }, timeout);
}

helpers.selectDropdown = function(elem, value) {
    elem.all(by.cssContainingText('option', value)).get(0).click();
};

helpers.adminUserLogin = function () {
    browser.get('/admin/').then(function () {
        element.all(by.css('#email')).get(0).sendKeys("test@example.org");
        element.all(by.css('#password')).get(0).sendKeys("password");
        element.all(by.css('form button[type=submit]')).click().then(function () {
            helpers.waitForUrl(/\/document\/list$/);
        });
    });
};

helpers.userLogin = function () {
    browser.get('/admin/').then(function () {
        element.all(by.css('#email')).get(0).sendKeys("testing@example.org");
        element.all(by.css('#password')).get(0).sendKeys("password");
        element.all(by.css('form button[type=submit]')).click();
        helpers.waitForUrl(/\/document\/list$/);
    });
};

helpers.clickUserMenu = function () {
    helpers.waitUntilDisplayed(by.css('.navbar li a'), 1).click();
    helpers.waitForUrl(/\/user\/list$/);
};

helpers.clickJobMenu = function () {
    helpers.waitUntilDisplayed(by.css('.navbar li a'), 2).click();
    helpers.waitForUrl(/\/job$/);
};

module.exports = helpers;
