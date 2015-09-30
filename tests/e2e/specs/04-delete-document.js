var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Delete Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
        });

        it('Document can be deleted', function () {
            helpers.waitForUrl(/\/document\/list$/);
            var elements;

            elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(1).getText().then(function (text) {
                    return text.trim() === browser.params.add_page.name + 'Updated';
                });
            });

            // click on delete button
            elements.first().all(by.css('button')).get(2).click().then(function () {
                element.all(by.css('.modal-footer .btn-primary')).get(0).click();
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

        it('Document cannot be deleted', function () {
            helpers.waitForUrl(/\/document\/list$/);
            var elements;

            elements = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(1).getText().then(function (text) {
                    return text.trim() === browser.params.add_page_parent.name;
                });
            });

            // click on delete button
            elements.first().all(by.css('button')).get(2).click().then(function () {
                expect(element.all(by.css('.alert')).count()).to.eventually.equal(1);
                element.all(by.css('.alert button')).get(0).click();
            });

        });

        after(function () {
            browser.get('/logout');
        });
    });

});
