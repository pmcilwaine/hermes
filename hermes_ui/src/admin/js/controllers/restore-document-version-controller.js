(function () {

    var dependencies, documentController;

    documentController = function (scope, $state, DocumentList, Documents) {
        scope.documents = DocumentList.documents;

        scope.restoreVersion = function (index) {
            var record = scope.documents[index];
            Documents.restoreVersion(record).then(function ok() {
                $state.go('document.list');
            });
        };
    };

    dependencies = [
        '$scope',
        '$state',
        'DocumentList',
        'Documents',
        documentController
    ];

    angular.module('hermes.controllers').controller('RestoreDocumentVersionController', dependencies);

})();