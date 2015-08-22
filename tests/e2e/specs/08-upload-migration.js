var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

describe.skip('Upload Migration File', function () {

    describe('Does not have permission', function () {

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