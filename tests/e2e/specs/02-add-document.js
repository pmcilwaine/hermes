var chai = require('chai');
chai.use(require('chai-as-promised'));

chai.should();
var expect = chai.expect;

var helpers = require('../../helpers/helpers.js');

var path = require('path');
var remote = require('protractor/node_modules/selenium-webdriver/remote');

describe('Add Document', function () {

    describe('Has Permission', function () {

        before(function () {
            helpers.adminUserLogin();
        });

        it('Can create a new page type document', function () {
            helpers.waitForUrl(/\/document\/list$/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                helpers.waitForUrl(/\/document\/add$/);

                helpers.waitUntilDisplayed(by.model('record.document.name')).sendKeys(browser.params.add_page.name)
                helpers.waitUntilDisplayed(by.model('record.document.menutitle')).sendKeys(browser.params.add_page.menutitle);
                helpers.waitUntilDisplayed(by.model('record.document.url')).clear();
                helpers.waitUntilDisplayed(by.model('record.document.url')).sendKeys(browser.params.add_page.url);

                var type = helpers.waitUntilDisplayed(by.model('record.document.type'));
                helpers.selectDropdown(type, browser.params.add_page.type);

                var template = helpers.waitUntilDisplayed(by.model('record.page.template'));
                helpers.selectDropdown(template, browser.params.add_page.template);

                var published = helpers.waitUntilDisplayed(by.model('record.document.published'));

                if (browser.params.add_page.published) {
                    published.click();
                }

                var show_in_menu = helpers.waitUntilDisplayed(by.model('record.document.show_in_menu'));

                if (browser.params.add_page.show_in_menu) {
                    show_in_menu.click();
                }

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    var iframe;
                    helpers.waitForUrl(/\/document\/page\/$/);

                    helpers.waitUntilDisplayed(by.css('iframe'));
                    iframe = browser.driver.findElement(by.css('iframe'));

                    browser.driver.switchTo().frame(iframe).then(function () {

                        var body = element(by.id('tinymce'));
                        body.clear();
                        body.click();
                        body.sendKeys(browser.params.add_page.content);

                        browser.driver.switchTo().defaultContent().then(function () {

                            helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                                helpers.waitForUrl(/\/document\/list$/);

                                var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                                    return elem.all(by.css('td')).get(1).getText().then(function (text) {
                                        return text === browser.params.add_page.name;
                                    });
                                });

                                expect(elements.count()).to.eventually.equal(1);
                            });

                        });

                    });

                });

            });
        });

        it('Can create new page type document with parent', function () {
            helpers.waitForUrl(/\/document\/list$/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                helpers.waitForUrl(/\/document\/add$/);

                var name = helpers.waitUntilDisplayed(by.model('record.document.name'));
                var menutitle = helpers.waitUntilDisplayed(by.model('record.document.menutitle'));
                var parent_name = helpers.waitUntilDisplayed(by.model('parent'));
                var url = helpers.waitUntilDisplayed(by.model('record.document.url'));
                var type = helpers.waitUntilDisplayed(by.model('record.document.type'));
                var published = helpers.waitUntilDisplayed(by.model('record.document.published'));
                var show_in_menu = helpers.waitUntilDisplayed(by.model('record.document.show_in_menu'));

                name.sendKeys(browser.params.add_page_parent.name);
                menutitle.sendKeys(browser.params.add_page_parent.menutitle);
                helpers.selectDropdown(parent_name, browser.params.add_page_parent.parent);

                url.clear();
                url.sendKeys(browser.params.add_page_parent.url);
                helpers.selectDropdown(type, browser.params.add_page_parent.type);

                var template = helpers.waitUntilDisplayed(by.model('record.page.template'));
                helpers.selectDropdown(template, browser.params.add_page_parent.template);

                if (browser.params.add_page_parent.published) {
                    published.click();
                }

                if (browser.params.add_page_parent.show_in_menu) {
                    show_in_menu.click();
                }

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    var iframe;
                    helpers.waitForUrl(/\/document\/page\/$/);

                    helpers.waitUntilDisplayed(by.css('iframe'));
                    iframe = browser.driver.findElement(by.css('iframe'));

                    browser.driver.switchTo().frame(iframe).then(function () {

                        var body = element(by.id('tinymce'));
                        body.clear();
                        body.click();
                        body.sendKeys(browser.params.add_page_parent.content);

                        browser.driver.switchTo().defaultContent().then(function () {

                            helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                                helpers.waitForUrl(/\/document\/list$/);

                                var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                                    return elem.all(by.css('td')).get(1).getText().then(function (text) {
                                        return text === browser.params.add_page_parent.name;
                                    });
                                });

                                expect(elements.count()).to.eventually.equal(1);
                            });

                        });

                    });

                });

            });
        });

        it('Can create a new file type document', function () {
            helpers.waitForUrl(/\/document\/list$/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                helpers.waitForUrl(/\/document\/add$/);

                var name = helpers.waitUntilDisplayed(by.model('record.document.name'));
                var parent_name = helpers.waitUntilDisplayed(by.model('parent'));
                var url = helpers.waitUntilDisplayed(by.model('record.document.url'));
                var type = helpers.waitUntilDisplayed(by.model('record.document.type'));
                var published = helpers.waitUntilDisplayed(by.model('record.document.published'));
                var show_in_menu = helpers.waitUntilDisplayed(by.model('record.document.show_in_menu'));

                name.sendKeys(browser.params.add_file.name);
                helpers.selectDropdown(parent_name, browser.params.add_file.parent);

                url.clear();
                url.sendKeys(browser.params.add_file.url);
                helpers.selectDropdown(type, browser.params.add_file.type);

                if (browser.params.add_file.published) {
                    published.click();
                }

                if (browser.params.add_file.show_in_menu) {
                    show_in_menu.click();
                }

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    helpers.waitForUrl(/\/document\/file\/$/);

                    var absolutePath = path.resolve('e2e/files', browser.params.add_file.file_path);
                    browser.setFileDetector(new remote.FileDetector);
                    helpers.waitUntilDisplayed(by.model('file')).sendKeys(absolutePath);

                    helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                        helpers.waitForUrl(/\/document\/list$/);

                        var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                            return elem.all(by.css('td')).get(1).getText().then(function (text) {
                                return text === browser.params.add_file.name;
                            });
                        });

                        expect(elements.count()).to.eventually.equal(1);
                    });
                });
            });

        });

        it('Can create a new multipage type document', function () {

            helpers.waitForUrl(/\/document\/list$/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                helpers.waitForUrl(/\/document\/add$/);

                var name = helpers.waitUntilDisplayed(by.model('record.document.name'));
                var parent_name = helpers.waitUntilDisplayed(by.model('parent'));
                var url = helpers.waitUntilDisplayed(by.model('record.document.url'));
                var type = helpers.waitUntilDisplayed(by.model('record.document.type'));
                var published = helpers.waitUntilDisplayed(by.model('record.document.published'));
                var show_in_menu = helpers.waitUntilDisplayed(by.model('record.document.show_in_menu'));

                name.sendKeys(browser.params.add_multipage.name);
                helpers.selectDropdown(parent_name, browser.params.add_multipage.parent);

                url.clear();
                url.sendKeys(browser.params.add_multipage.url);
                helpers.selectDropdown(type, browser.params.add_multipage.type);

                if (browser.params.add_multipage.published) {
                    published.click();
                }

                if (browser.params.add_multipage.show_in_menu) {
                    show_in_menu.click();
                }

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    helpers.waitForUrl(/\/document\/multipage\/$/);

                    var absolutePath = path.resolve('e2e/files', browser.params.add_multipage.file_path);
                    browser.setFileDetector(new remote.FileDetector);
                    helpers.waitUntilDisplayed(by.model('file')).sendKeys(absolutePath);

                    helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                        helpers.waitForUrl(/\/document\/list$/);

                        var elements = element.all(by.css('tbody tr')).filter(function (elem) {
                            return elem.all(by.css('td')).get(1).getText().then(function (text) {
                                return text === browser.params.add_multipage.name;
                            });
                        });

                        expect(elements.count()).to.eventually.equal(1);
                    });
                });

            });

        });

        it.skip('Invalid URL when creating a Document based on Multipage Document URL', function () {

        });

        it('Error message displayed on invalid URL document', function () {
            helpers.waitForUrl(/\/document\/list$/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                helpers.waitForUrl(/\/document\/add/);

                var name = helpers.waitUntilDisplayed(by.model('record.document.name'));
                var menutitle = helpers.waitUntilDisplayed(by.model('record.document.menutitle'));
                var url = helpers.waitUntilDisplayed(by.model('record.document.url'));
                var type = helpers.waitUntilDisplayed(by.model('record.document.type'));
                var published = helpers.waitUntilDisplayed(by.model('record.document.published'));
                var show_in_menu = helpers.waitUntilDisplayed(by.model('record.document.show_in_menu'));

                name.sendKeys(browser.params.add_page.name);
                menutitle.sendKeys(browser.params.add_page.menutitle);
                url.clear();
                url.sendKeys(browser.params.add_page.url);

                helpers.selectDropdown(type, browser.params.add_page.type);

                var template = helpers.waitUntilDisplayed(by.model('record.page.template'));
                helpers.selectDropdown(template, browser.params.add_page.template);

                if (browser.params.add_page.published) {
                    published.click();
                }

                if (browser.params.add_page.show_in_menu) {
                    show_in_menu.click();
                }

                helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                    helpers.waitForUrl(/\/document\/add/);

                    var elements = element.all(by.css('p.help-block')).filter(function (elem) {
                        return elem.getText().then(function (text) {
                            return 'URL is already in use' === text;
                        });
                    });

                    expect(elements.count()).to.eventually.equal(1);
                });

            });
        });

        it('Validation message is displayed on blank form', function () {
            browser.get('/admin/').then(function () {
                helpers.waitForUrl(/\/document\/list$/);
                helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                    helpers.waitForUrl(/\/document\/add$/);

                    helpers.waitUntilDisplayed(by.css('button[type=submit]')).click().then(function () {
                        expect(browser.getLocationAbsUrl()).to.eventually.match(/\/document\/add/);
                        expect(element.all(by.css('.has-error')).count()).to.eventually.be.at.least(1);
                    });

                });
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

        it('Cannot create a new document', function () {
            helpers.waitForUrl(/\/document\/list$/);
            helpers.waitUntilDisplayed(by.css('button'), 1).click().then(function () {
                expect(element.all(by.css('.alert')).count()).to.eventually.equal(1);
                element.all(by.css('.alert button')).get(0).click();
            });
        });

        after(function () {
            browser.get('/logout');
        });
    });

});
