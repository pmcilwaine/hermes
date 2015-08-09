var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Add Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
        });

        it('Can create a new page type document', function () {
            helpers.waitUntilDisplayed(by.css('button')).click().then(function () {

                var name = helpers.waitUntilDisplayed(by.model('record.document.name'));
                var menutitle = helpers.waitUntilDisplayed(by.model('record.document.menutitle'));
                var url = helpers.waitUntilDisplayed(by.model('record.document.url'));
                var type = helpers.waitUntilDisplayed(by.model('record.document.type'));
                var published = helpers.waitUntilDisplayed(by.model('record.document.published'));
                var show_in_menu = helpers.waitUntilDisplayed(by.model('record.document.show_in_menu'));

                name.sendKeys(browser.params.add_page.name);
                menutitle.sendKeys(browser.params.add_page.menutitle);
                url.sendKeys(browser.params.add_page.url);

                helpers.selectDropdown(type, browser.params.add_page.type);

                var template = helpers.waitUntilDisplayed(by.model('record.page.template'));
                helpers.selectDropdown(template, browser.params.add_page.template);

                if (browser.params.add_page.published) {
                    published.click();
                }

                if (browser.params.add_page.show_in_menu) {
                    show_in_menu.click();
                }

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {

                    helpers.waitUntilDisplayed(by.model('record.page.content')).sendKeys(browser.params.add_page.content);

                    helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                        browser.wait(function () {
                            return browser.getLocationAbsUrl().then(function (url) {
                                return url.match(/\/document\/list$/);
                            });
                        }, 30000);

                        var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                            return elem.all(by.css('td')).get(1).getText().then(function (text) {
                                return text === browser.params.add_page.name;
                            });
                        });

                        expect(elements.count()).to.eventually.equal(1);
                    });

                });

            });

        });

        it.skip('Can create a new file type document', function () {

        });

        it.skip('Can create a new multipage type document', function () {

        });

        it.skip('Error message displayed on invalid URL document', function () {

        });

        it.skip('Validation message is displayed on blank form', function () {

        });

        after(function () {
            browser.get('/logout');
        });
    });

    describe('Does not have permission', function () {

        it.skip('Cannot create a new document', function () {

        });

    });

});
