(function () {

    var dependencies, documentService;

    documentService = function (DocumentResource) {
        var document = {}, currentLoaded ;

        document.getNextPage = function () {

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
        'DocumentResource',
        documentService
    ];

    angular.module('hermes.services').factory('Documents', dependencies);

})();