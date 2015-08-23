var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Add User', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
            helpers.clickUserMenu();
        });

        it('Can create a new user account', function () {
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {

                helpers.waitUntilDisplayed(by.model('record.email')).sendKeys(browser.params.add_user.email);
                helpers.waitUntilDisplayed(by.model('record.password')).sendKeys(browser.params.add_user.password);
                helpers.waitUntilDisplayed(by.model('record.first_name')).sendKeys(browser.params.add_user.first_name);
                helpers.waitUntilDisplayed(by.model('record.last_name')).sendKeys(browser.params.add_user.last_name);

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click();
            });
        });

        it('Email address already exists', function () {
            helpers.waitForUrl(/\/user\/list/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                helpers.waitForUrl(/\/user\/add$/);

                helpers.waitUntilDisplayed(by.model('record.email')).sendKeys(browser.params.add_user.email);
                helpers.waitUntilDisplayed(by.model('record.password')).sendKeys(browser.params.add_user.password);
                helpers.waitUntilDisplayed(by.model('record.first_name')).sendKeys(browser.params.add_user.first_name);
                helpers.waitUntilDisplayed(by.model('record.last_name')).sendKeys(browser.params.add_user.last_name);

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    helpers.waitForUrl(/\/user\/add$/);

                    var elements = element.all(by.css('p.help-block')).filter(function (elem) {
                        return elem.getText().then(function (text) {
                            return 'Email address already in use' === text;
                        });
                    });

                    expect(elements.count()).to.eventually.be.equal(1);
                });

            });

        });

        after(function () {
            browser.get('/logout');
        });
    });

    /*describe('Does not have permission', function () {

        before(function () {
            helpers.userLogin();
            helpers.clickUserMenu();
        });

        it.skip('Cannot create new user account', function () {

        });

        after(function () {
            browser.get('/logout');
        });
    });*/

});
