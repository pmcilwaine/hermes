var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe('Upload Migration File', function () {

    describe.skip('Does not have permission', function () {

        before(function () {
            helpers.userLogin();
        });

        it('Cannot upload a data migration file', function () {

        });

        after(function () {
            browser.get('/logout');
        });

    });

});