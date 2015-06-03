var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Login', function () {

    before(function () {
        isAngularSite(false);
    })

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

});
