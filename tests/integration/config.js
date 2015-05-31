exports.config = {
    framework: 'mocha',
    mochaOpts: {
        reporter: 'spec',
        timeout: 600000,
        reporter: "mocha-jenkins-reporter",
        reporterOptions: {
            junit_report_name: "Integration Tests",
            junit_report_path: "report.xml",
            junit_report_stack: 1
        }
    },
    specs: 'specs/*.js',
    getPageTimeout:600000,
    allScriptsTimeout: 99999
};