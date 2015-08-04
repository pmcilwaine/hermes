(function () {

    var dependencies, jobController;

    jobController = function (scope, JobResource) {
        scope.jobs = [];

        JobResource.get(function (response) {
            scope.jobs = response.jobs;
        });
    };

    dependencies = [
        '$scope',
        'JobResource',
        jobController
    ];

    angular.module('hermes.controllers').controller('JobListController', dependencies);

})();