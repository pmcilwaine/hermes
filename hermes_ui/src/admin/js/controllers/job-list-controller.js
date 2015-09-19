(function () {

    var dependencies, jobController;

    jobController = function (scope, jobs, DownloadUrlResource, $window) {
        scope.jobs = jobs.jobs;

        scope.download = function (index) {
            console.log(scope.jobs[index].message.download);
            DownloadUrlResource.post(scope.jobs[index].message.download, function ok (response) {
                $window.open(response.url);
            }, function fail (response) {
                console.log('failed download url');
                console.log(response);
            });
        };
    };

    dependencies = [
        '$scope',
        'jobs',
        'DownloadUrlResource',
        '$window',
        jobController
    ];

    angular.module('hermes.controllers').controller('JobListController', dependencies);

})();