var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Login', function () {

    describe('Login to Site', function () {

        beforeEach(function () {
            browser.get('/login');
        });

        it('Test Invalid Login', function () {
            element.all(by.css('#email')).get(0).sendKeys("invalid-user@example.org");
            element.all(by.css('#password')).get(0).sendKeys("5a4d5a4dasda dasdasd");
            element.all(by.css('form button[type=submit]')).click();
            expect(element.all(by.css('.alert')).count()).to.eventually.equal(1);
        });

        it('Test Valid Login', function () {
            element.all(by.css('#email')).get(0).sendKeys("test@example.org");
            element.all(by.css('#password')).get(0).sendKeys("password");
            element.all(by.css('form button[type=submit]')).click();
            expect(browser.getCurrentUrl()).to.eventually.equal(process.env.BASE_URL + '/');
        });

        afterEach(function () {
            browser.get('/logout');
        });

    });

    describe('Login to Admin', function () {

        beforeEach(function () {
            browser.get('/admin/');
        });

        it('Test redirected to login', function () {
            expect(browser.getCurrentUrl()).to.eventually.equal(process.env.BASE_URL + '/login?next_page=%2Fadmin%2F%3F');
        });

        it('Not logged Administrator with redirection', function () {
            element.all(by.css('#email')).get(0).sendKeys("test@example.org");
            element.all(by.css('#password')).get(0).sendKeys("password");
            element.all(by.css('form button[type=submit]')).click();
            expect(browser.getCurrentUrl()).to.eventually.equal(process.env.BASE_URL + '/admin/#/document/list');
        });

        afterEach(function () {
            browser.get('/logout');
        });

    });

});
