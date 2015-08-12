var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe.skip('Restore Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
            helpers.waitUntilDisplayed(by.css('button'), 3).click();
            helpers.waitForUrl(/\/document\/restore/);
        });

        it('Can restore document', function () {
            var elements, name = browser.params.add_page.name + 'Updated'.trim();
            helpers.waitForUrl(/\/document\/restore/);

            elements = $$('tbody tr').filter(function (elem) {
                return elem.all(by.css('td')).get(1).getText().then(function (text) {
                    return text.trim() === name;
                });
            });

            elements.get(0).all(by.css('button')).get(0).click().then(function () {

                var items = $$('tbody tr').filter(function (elem) {
                    return elem.all(by.css('td')).get(1).getText().then(function (text) {
                        return text.trim() === name;
                    });
                });

                helpers.waitForUrl(/\/document\/restore/);
                expect(items.count()).to.eventually.equal(0);
            });
        });

        after(function () {
            browser.get('/logout');
        });
    });

});
