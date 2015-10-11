(function () {

    var dependencies, documentController;

    documentController = function (scope, $state, DocumentList, Documents) {
        scope.documents = DocumentList.documents;

        scope.documents.forEach(function (document) {
            document.created = moment.utc(document.created,
                'YYYY-MM-DD HH:mm:ss').tz('Australia/Sydney').format('MMMM Do YYYY, h:mm:ss a');
        });

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