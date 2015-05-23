var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var mockHttp = require('./mocks/httpMock.js');
var helpers = require('../../helpers/helpers.js');

var path = require('path');

describe('Documents', function () {

    before(function () {
        mockHttp.register();
        this.timeout(0);
        browser.get('/#/document/list');
    });

    it('Has a list of documents', function () {
        expect(element.all(by.css('table tbody tr')).count()).to.eventually.equal(1);
    });

    it('Record contains values', function () {
        var row = element.all(by.repeater('document in documents')).get(0);
        var columns = row.all(by.css('td'));
        expect(columns.get(0).getText()).to.eventually.equal("Homepage");
        expect(columns.get(1).getText()).to.eventually.equal("index");
    });

    it('Create Page Type Document', function () {
        element.all(by.css('button')).get(0).click();

        var name = element(by.model('record.document.name'));
        var url = element(by.model('record.document.url'));
        var type = element(by.model('record.document.type'));

        name.sendKeys("First Document");
        url.sendKeys("first-document");
        helpers.selectDropdown(type, 'Page');

        var template = element(by.model('record.page.template'));
        helpers.selectDropdown(template, 'Standard');

        element.all(by.css('button')).get(0).click();

        var content = element(by.model('record.page.content'));
        content.sendKeys('<p>Content for page</p>');
        element.all(by.css('button')).get(0).click();
        expect(element.all(by.css('table tbody tr')).count()).to.eventually.equal(2);
    });

    it('Create File Type Document', function () {
        element.all(by.css('button')).get(0).click();

        var name = element(by.model('record.document.name'));
        var url = element(by.model('record.document.url'));
        var type = element(by.model('record.document.type'));

        name.sendKeys("First File");
        url.sendKeys("first-file");
        helpers.selectDropdown(type, 'File');

        element.all(by.css('button')).get(0).click();

        var file = element(by.model('file'));

        var fileToUpload = '../../data/test_cases.dot',
            absolutePath = path.resolve(__dirname, fileToUpload);

        file.sendKeys(absolutePath);
        element.all(by.css('button')).get(0).click();
        expect(element.all(by.css('table tbody tr')).count()).to.eventually.equal(3);
    });

    after(function() {
        browser.takeScreenshot()
    });

});