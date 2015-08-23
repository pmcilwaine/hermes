var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var mockHttp = require('./mocks/httpMock.js');
var helpers = require('../../helpers/helpers.js');

describe.skip('Users', function () {

    before(function () {
        mockHttp.register();
        this.timeout(0);
        browser.get('/#/user/list');
    });

    it('Has a list of users', function () {
        expect(element.all(by.css('table tbody tr')).count()).to.eventually.equal(1);
    });

    it('Record contains values', function () {
        var row = element.all(by.repeater('user in users')).get(0);
        var columns = row.all(by.css('td'));

        expect(columns.get(0).getText()).to.eventually.equal("test@example.org");
        expect(columns.get(1).getText()).to.eventually.equal("Test");
        expect(columns.get(2).getText()).to.eventually.equal("User");
    });

    it('Can click on edit button', function () {
        var row = element.all(by.repeater('user in users')).get(0);
        var columns = row.all(by.css('td'));
        columns.get(3).all(by.css('button')).get(0).click();
        expect(browser.getLocationAbsUrl()).to.eventually.match(/\/user\/modify\/1/);
    });

    it('Record Values in Modify Form', function () {
        var email = element(by.model('record.email'));
        var first_name = element(by.model('record.first_name'));
        var last_name = element(by.model('record.last_name'));

        expect(email.getAttribute('value')).to.eventually.equal("test@example.org");
        expect(first_name.getAttribute('value')).to.eventually.equal("Test");
        expect(last_name.getAttribute('value')).to.eventually.equal("User");
    });

    it('Save Existing Record', function () {
        var first_name = element(by.model('record.first_name'));
        first_name.clear().then(function () {
            first_name.sendKeys("My First Name");

            helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                var row = element.all(by.repeater('user in users')).get(0);
                var columns = row.all(by.css('td'));
                expect(columns.get(1).getText()).to.eventually.equal("My First Name");
            });
        });
    });

    it('Create New User', function () {
        expect(browser.getLocationAbsUrl()).to.eventually.match(/\/user\/list/);
        element.all(by.css('button')).get(1).click();
        expect(browser.getLocationAbsUrl()).to.eventually.match(/\/user\/add/);

        var email = element(by.model('record.email'));
        var password = element(by.model('record.password'));
        var first_name = element(by.model('record.first_name'));
        var last_name = element(by.model('record.last_name'));

        email.sendKeys('new_user@example.org');
        password.sendKeys('password');
        first_name.sendKeys('Tester');
        last_name.sendKeys('User');

        element.all(by.css('button')).get(0).click();
        expect(element.all(by.css('table tbody tr')).count()).to.eventually.equal(2);
    });

    it('Delete User', function () {
        var row = element.all(by.repeater('user in users')).get(1);
        var columns = row.all(by.css('td'));
        columns.last().all(by.css('button')).last().click();
        expect(element.all(by.css('table tbody tr')).count()).to.eventually.equal(1);
    });

    after(function() {
        try {
            browser.takeScreenshot();
        } catch (e) {

        }
    });

});
