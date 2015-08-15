var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Restore Version Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
        });

        it('A deleted document is restored', function () {
            var name = browser.params.add_page.name + 'Updated', elements;
            helpers.waitForUrl(/\/document\/list$/);

            elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(1).getText().then(function (text) {
                    return text.trim() === name;
                });
            });

            expect(elements.count()).to.eventually.be.equal(1);

            elements.get(0).all(by.css('button')).get(0).click().then(function () {
                var items;
                helpers.waitForUrl(/\/document\/version/);

                items = element.all(by.css('tbody tr')).filter(function (elem) {
                    return elem.all(by.css('td')).get(0).getText().then(function (text) {
                        return text.trim() === browser.params.add_page.name;
                    })
                });

                expect(items.count()).to.eventually.be.equal(1);
                items.get(0).all(by.css('button')).get(0).click(function () {
                    helpers.waitForUrl(/\/document\/list$/);

                    elements = element.all(by.css('tbody tr')).filter(function (elem) {
                        return elem.all(by.css('td')).get(1).getText().then(function (text) {
                            return text.trim() === browser.params.add_page.name;
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

});