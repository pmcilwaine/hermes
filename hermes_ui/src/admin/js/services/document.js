(function () {

    var dependencies, documentService;

    documentService = function ($q, DocumentResource) {
        var document = {}, new_document = {};

        document.getNextPage = function () {

        };

        document.createNewDocument = function (record) {
            new_document = record;
        }

        document.getNewDocument = function () {
            var d = new_document;
            new_document = {};
            return d;
        };

        document.dryRun = function (record) {
            return this.save(record, true);
        }

        document.save = function (record, is_dry_run) {
            var deferred = $q.defer();
            if (is_dry_run !== undefined) {
                return DocumentResource.dryRun(record, function ok (msg) {
                    console.log('ok dryrun');
                    console.log(msg);
                    deferred.resolve(msg);
                }, function fail (msg) {
                    console.log('fail dryrun');
                    console.log(msg);
                    deferred.reject(msg);
                });
            } else {
                return DocumentResource.post(record, function ok (msg) {
                    console.log('ok save');
                    console.log(msg);
                    deferred.resolve(msg);
                }, function fail (msg) {
                    console.log('fail save');
                    console.log(msg);
                    deferred.reject(msg);
                });
            }

            return deferred.promise;
        };

        document.get = function (offset, limit) {
            offset = offset || 0;
            limit = limit || 100;

            return DocumentResource.get({offset: offset, limit: limit}).$promise.then(function (documents) {
                return documents;
            });
        };

        return document;
    };

    dependencies = [
        '$q',
        'DocumentResource',
        documentService
    ];

    angular.module('hermes.services').factory('Documents', dependencies);

})();