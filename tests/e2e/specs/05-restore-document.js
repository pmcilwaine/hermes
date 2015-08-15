var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Restore Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
            helpers.waitUntilDisplayed(by.css('button'), 3).click();
            helpers.waitForUrl(/\/document\/restore/);
        });

        it('Can restore document', function () {
            var elements, name = browser.params.add_page.name + 'Updated'.trim(), items;
            helpers.waitForUrl(/\/document\/restore/);

            elements = $$('tbody tr').filter(function (elem) {
                return elem.all(by.css('td')).get(0).getText().then(function (text) {
                    return text.trim() === name;
                });
            });

            expect(elements.count()).to.eventually.equal(1);

            elements.get(0).all(by.css('button')).get(0).click().then(function () {
                helpers.waitUntilDisplayed(by.css('button')).click(function () {
                    helpers.waitForUrl(/\/document\/list$/);

                    var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                        return elem.all(by.css('td')).get(1).getText().then(function (text) {
                            return text.trim() === name;
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

});
