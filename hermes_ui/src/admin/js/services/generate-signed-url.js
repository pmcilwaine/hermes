(function () {

    var dependencies, signedUrlService;

    signedUrlService = function (UploadUrlResource, $q) {
        var service = {};

        service.newUploadUrl = function () {
            var deferred = $q.defer();
            UploadUrlResource.post({}, function ok (msg) {
                deferred.resolve(msg);
            }, function fail (msg) {
                deferred.reject(msg);
            });
            return deferred.promise;
        };

        return service;
    };

    dependencies = [
        'UploadUrlResource',
        '$q',
        signedUrlService
    ];

    angular.module('hermes.services').factory('GenerateUrl', dependencies);

})();