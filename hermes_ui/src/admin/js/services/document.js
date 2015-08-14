(function () {

    var dependencies, documentService;

    documentService = function ($q, DocumentResource, RestoreDocumentResource) {
        var document = {}, new_document = {};

        document.getNextPage = function () {

        };

        document.getAllWithRepeat = function (repeat_str) {
            return document.getAll().then(function (response) {
                _.each(response.documents, function (document) {
                    var repeat = document.path.split(/\//).length - 2;
                    document.name = _.repeat(repeat_str, 3 * repeat) + document.name;
                });
                return response.documents;
            });
        };

        document.createNewDocument = function (record) {
            new_document = record;
        };

        document.getNewDocument = function () {
            var d = new_document;
            new_document = {};
            return d;
        };

        document.dryRun = function (record) {
            return this.save(record, true);
        };

        document.save = function (record, is_dry_run) {
            var deferred = $q.defer(), method;
            if (is_dry_run !== undefined) {
                DocumentResource.dryRun(record, function ok (msg) {
                    console.log('ok dryRun');
                    deferred.resolve(msg.data);
                }, function fail (msg) {
                    console.log('fail dryRun');
                    console.log(msg);
                    deferred.reject(msg.data);
                });
            } else {
                if (!record.document.uuid) {
                    method = DocumentResource.post;
                } else {
                    method = DocumentResource.put;
                }

                method(record, function ok(msg) {
                    deferred.resolve(msg);
                }, function fail(msg) {
                    deferred.reject(msg);
                });
            }

            return deferred.promise;
        };

        document.getDocument = function (uuid) {
            return DocumentResource.get({id: uuid}).$promise.then(function (document) {
                return document;
            });
        };

        document.deleteById = function (document_id) {
            var deferred = $q.defer();
            DocumentResource.delete({id: document_id}, function ok (msg) {
                deferred.resolve(msg);
            }, function fail (msg) {
                deferred.reject(msg);
            });

            return deferred.promise;
        };

        document.getAll = function (offset, limit) {
            offset = offset || 0;
            limit = limit || 100;

            return DocumentResource.get({offset: offset, limit: limit}).$promise.then(function (documents) {
                return documents;
            });

        };

        document.getAllRestore = function (offset, limit) {
            offset = offset || 0;
            limit = limit || 100;

            return RestoreDocumentResource.get({offset: offset, limit: limit}).$promise.then(function (documents) {
                return documents;
            });
        };

        return document;
    };

    dependencies = [
        '$q',
        'DocumentResource',
        'RestoreDocumentResource',
        documentService
    ];

    angular.module('hermes.services').factory('Documents', dependencies);

})();