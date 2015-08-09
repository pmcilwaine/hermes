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

helpers.selectDropdown = function(elem, value) {
    elem.all(by.cssContainingText('option', value)).get(0).click();
};

helpers.adminUserLogin = function () {
    browser.get('/admin/').then(function () {
        element.all(by.css('#email')).get(0).sendKeys("test@example.org");
        element.all(by.css('#password')).get(0).sendKeys("password");
        element.all(by.css('form button[type=submit]')).click();
    });
};

helpers.userLogin = function () {
    browser.get('/admin/').then(function () {
        element.all(by.css('#email')).get(0).sendKeys(browser.params.add_user.email);
        element.all(by.css('#password')).get(0).sendKeys(browser.params.add_user.password);
        element.all(by.css('form button[type=submit]')).click();
    });
};

helpers.clickUserMenu = function () {
    helpers.waitUntilDisplayed(by.css('.navbar li a'), 1).click();
};

module.exports = helpers;
