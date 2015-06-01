(function () {

    var dependencies, documentController;

    documentController = function (scope, DocumentList, Documents) {
        scope.documents = DocumentList.documents;


        scope.deleteItem = function (index) {
            var record = scope.documents[index];
            Documents.deleteById(record.uuid).then(function ok () {
                scope.documents.splice(index, 1);
            }, function fail (msg) {
                console.log('Delete Failed');
                console.log(msg);
            });
        };
    };

    dependencies = [
        '$scope',
        'DocumentList',
        'Documents',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentListController', dependencies);

})();