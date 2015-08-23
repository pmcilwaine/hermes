(function () {

    var dependencies, documentController;

    documentController = function (scope, DocumentList, RestoreDocumentResource) {
        scope.documents = DocumentList.documents;

        scope.restoreItem = function (index) {
            var record = scope.documents[index];
            RestoreDocumentResource.put(record, function ok () {
                scope.documents.splice(index, 1);
            }, function fail (msg) {
                console.log('Restore Document Failed');
                console.log(msg);
            });
        };
    };

    dependencies = [
        '$scope',
        'DocumentList',
        'RestoreDocumentResource',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentRestoreController', dependencies);

})();