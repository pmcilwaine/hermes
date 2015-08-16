var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Download Migration', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
        });

        it('Create Download Migration Job', function () {
            helpers.waitForUrl(/\/document\/list$/);
            var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(1).getText().then(function (text) {
                    return text.trim() === browser.params.add_page.name;
                });
            });

            expect(elements.count()).to.eventually.be.equal(1);

            elements.get(0).all(by.css('input')).get(0).click().then(function () {
                helpers.waitUntilDisplayed(by.css('button'), 3).click();

                helpers.waitUntilDisplayed(by.css('input[name=name]')).sendKeys(browser.params.migration_download.name);
                helpers.waitUntilDisplayed(by.css('.modal-footer button')).click();

                expect(element.all(by.css('.alert')).count()).to.eventually.equal(1);
            });
        });

        after(function () {
            browser.get('/logout');
        });
    });

    describe('Does not have permission', function () {

        before(function () {
            helpers.userLogin();
        });

        after(function () {
            browser.get('/logout');
        });
    });


});