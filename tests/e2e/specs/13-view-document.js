var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe.skip('View Document', function () {

    describe('Can View Document', function () {

        before(function () {
            browser.get('/' + browser.params.add_page.url);
        });

        it('Document is Displayed', function () {
            expect(element.all(by.css('h1')).get(0).getText()).to.eventually.equal(browser.params.add_page.name);
        });

    });

    describe('404', function () {

        before(function () {
            browser.get('/page-does-not-exist');
        });

        it('404 Page Displayed', function () {
            expect(element.all(by.css('h1')).get(0).getText()).to.eventually.equal("Page not found");
        });

    });

    it.skip('Can download a File Type Document', function () {

    });

    it.skip('Can view Multipage Type Document', function () {

    });

});
