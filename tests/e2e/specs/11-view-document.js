var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('View Document', function () {

    it.skip('Can View Document', function () {

    });

    it('404 Page Displayed', function () {
        browser.get('/page-does-not-exist').then(function () {
            expect(element.all(by.css('h1')).get(0).getText()).to.eventually.equal("Page not found")
        });
    });

    it.skip('Can download a File Type Document', function () {

    });

});
