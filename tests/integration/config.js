exports.config = {
    framework: 'mocha',
    mochaOpts: {
        reporter: 'spec',
        timeout: 600000,
        reporter: "mocha-junit-reporter",
        reporterOptions: {
            mochaFile: "report-integration.xml",
            junit_report_name: "Integration Tests",
            junit_report_path: "report-integration.xml",
            junit_report_stack: 1
        }
    },
    specs: 'specs/*.js',
    getPageTimeout:600000,
    allScriptsTimeout: 99999
};