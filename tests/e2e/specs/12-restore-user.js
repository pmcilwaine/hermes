var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Restore User', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
            helpers.clickUserMenu();
            helpers.waitUntilDisplayed(by.css('button'), 2).click();
            helpers.waitForUrl(/\/user\/restore/);
            console.log('restore');
        });

        it('Can restore user account', function () {
            var elements;

            helpers.waitUntilDisplayed(by.css("tbody tr"));
            expect(element.all(by.css("tbody tr")).count()).to.eventually.be.at.least(1);

            elements = element.all(by.css("tbody tr")).filter(function (elem) {
                return elem.all(by.css("td")).get(0).getText().then(function (text) {
                    return text.trim() === browser.params.add_user.email;
                });
            });

            elements.get(0).all(by.css('button')).get(0).click().then(function () {
                var items;

                items = element.all(by.css("tbody tr")).filter(function (elem) {
                    return elem.all(by.css("td")).get(0).getText().then(function (text) {
                        return text.trim() === browser.params.add_user.email;
                    });
                });

                expect(items.count()).to.eventually.equal(0);
            });
        });

        after(function () {
            browser.get('/logout');
        });
    });

});
