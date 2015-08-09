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
            element.all(by.cssContainingText('button', 'Add User')).get(0).click();

            var email = element(by.model('record.email'));
            var pasword = element(by.model('record.password'));
            var first_name = element(by.model('record.first_name'));
            var last_name = element(by.model('record.last_name'));

            email.sendKeys(browser.params.add_user.email);
            pasword.sendKeys(browser.params.add_user.password);
            first_name.sendKeys(browser.params.add_user.first_name);
            last_name.sendKeys(browser.params.add_user.last_name);

            helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                expect(browser.getLocationAbsUrl()).to.eventually.match(/\/user\/list/);

                var elements = element.all(by.repeater('user in users')).filter(function (elem) {
                    return elem.all(by.css('td')).get(0).getText().then(function (text) {
                        return text === browser.params.add_user.email;
                    });
                });

                expect(elements.count()).to.eventually.equal(1);
            });
        });

        it('Email address already exists', function () {
            element.all(by.cssContainingText('button', 'Add User')).get(0).click();

            var email = element(by.model('record.email'));
            var pasword = element(by.model('record.password'));
            var first_name = element(by.model('record.first_name'));
            var last_name = element(by.model('record.last_name'));

            email.sendKeys(browser.params.add_user.email);
            pasword.sendKeys(browser.params.add_user.password);
            first_name.sendKeys(browser.params.add_user.first_name);
            last_name.sendKeys(browser.params.add_user.last_name);

            helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                expect(browser.getLocationAbsUrl()).to.eventually.match(/\/user\/add/);

                var elements = element.all(by.css('p.help-block')).filter(function (elem) {
                    return elem.getText().then(function (text) {
                        return 'Email address already in use' === text;
                    });
                });

                expect(elements.count()).to.eventually.equal(1);
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
