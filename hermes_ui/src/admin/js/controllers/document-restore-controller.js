(function () {

    var dependencies, documentController;

    documentController = function (scope, DocumentList, RestoreDocumentResource) {
        scope.documents = DocumentList.documents;

        scope.documents.forEach(function (document) {
            document.created = moment(document.created, 'YYYY-MM-DD HH:mm:ss').add(10, 'hours').format('MMMM Do YYYY, h:mm:ss a');
        })

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