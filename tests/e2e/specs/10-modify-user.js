var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Modify User', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
            helpers.clickUserMenu();
        });

        it('Can Modify First and Last name', function () {

            helpers.waitForUrl(/\/user\/list$/);
            var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(0).getText().then(function (text) {
                    return text.trim() === browser.params.add_user.email;
                });
            });

            // click on edit button
            expect(elements.count()).to.eventually.be.equal(1);

            elements.get(0).all(by.css('button')).get(0).click().then(function () {
                helpers.waitForUrl(/\/user\/modify/);

                helpers.waitUntilDisplayed(by.model('record.first_name')).clear();
                helpers.waitUntilDisplayed(by.model('record.last_name')).clear();

                helpers.waitUntilDisplayed(by.model('record.first_name')).sendKeys(browser.params.modify_user.first_name);
                helpers.waitUntilDisplayed(by.model('record.last_name')).sendKeys(browser.params.modify_user.last_name);

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    helpers.waitForUrl(/\/user\/list$/);

                    var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                        return elem.all(by.css('td')).get(1).getText().then(function (text) {
                            return text.trim() === browser.params.modify_user.first_name;
                        });
                    });

                    expect(elements.count()).to.eventually.equal(1);
                });

            });

        });

        after(function () {
            browser.get('/logout');
        });
    });

    describe('Does not have permission', function () {

        before(function () {
            helpers.userLogin();
            helpers.clickUserMenu();
        });

        it('Cannot modify user', function () {
            helpers.waitForUrl(/\/user\/list$/);
            var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(0).getText().then(function (text) {
                    return text.trim() === browser.params.add_user.email;
                });
            });

            // click on edit button
            expect(elements.count()).to.eventually.be.equal(1);

            elements.get(0).all(by.css('button')).get(0).click().then(function () {
                expect(element.all(by.css('.alert')).count()).to.eventually.equal(1);
                element.all(by.css('.alert button')).get(0).click();
            });
        });

        after(function () {
            browser.get('/logout');
        });
    });

});
