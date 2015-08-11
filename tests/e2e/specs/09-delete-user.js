var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Delete User', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
            helpers.clickUserMenu();
        });

        it('Account can be deleted', function () {
            var item = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(0).getText().then(function (text) {
                    return text.trim() === browser.params.add_user.email;
                });
            });

            item.all(by.css('button')).get(1).click();

            item = element.all(by.css('tbody tr')).filter(function (elem) {
                return elem.all(by.css('td')).get(0).getText().then(function (text) {
                    return text.trim() === browser.params.add_user.email;
                });
            });

            expect(item.count()).to.eventually.equal(0);
        });

        after(function () {
            browser.get('/logout');
        });
    });

});