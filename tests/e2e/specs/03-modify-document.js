var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Modify Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
        });

        it('Can modify Page Type Document', function () {
            var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(1).getText().then(function (text) {
                    return text.trim() === browser.params.add_page.name;
                });
            });

            // click on edit button
            expect(elements.count()).to.eventually.be.equal(1);

            elements.get(0).all(by.css('button')).get(1).click().then(function () {
                var name = helpers.waitUntilDisplayed(by.model('record.document.name')),
                    name_str = browser.params.add_page.name + ' Updated'.trim();

                name.clear();
                name.sendKeys(name_str);

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {

                    browser.wait(function () {
                        return browser.getLocationAbsUrl().then(function (url) {
                            return url.match(/\/document\/list$/);
                        });
                    }, 30000);

                    var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                        return elem.all(by.css('td')).get(1).getText().then(function (text) {
                            return text.trim() === name_str;
                        });
                    });

                    expect(elements.count()).to.eventually.equal(1);

                });
            });
        });

        it.skip('Can modify File Type Document', function () {

        });

        it.skip('Can modify Multipage Type Document', function () {

        });

        after(function () {
            browser.get('/logout');
        });
    });

});
