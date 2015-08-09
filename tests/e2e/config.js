exports.config = {
    framework: 'mocha',
    mochaOpts: {
        timeout: 600000,
        allScriptsTimeout: 99999,
        reporter: "mocha-junit-reporter",
        reporterOptions: {
            mochaFile: "report-e2e.xml",
            junit_report_name: "End-to-End Tests",
            junit_report_path: "report-e2e.xml",
            junit_report_stack: 1
        }
    },
    specs: 'specs/*.js',
    getPageTimeout:600000,
    allScriptsTimeout: 99999,
    maxSessions: 2,
    onPrepare: function () {
        browser.ignoreSynchronization = true;

        browser.getCapabilities().then(function (cap) {
            browser.params = require('./profile/' + cap.caps_.platform.split(' ')[0].toLowerCase() +
            '/' + cap.caps_.browserName.split(' ')[0].toLowerCase() + '/data.js').data;
        });
    }
};