(function () {

    var dependencies, documentController;

    documentController = function (scope, DocumentList, Documents, MigrationDownload) {
        scope.documents = DocumentList.documents;
        scope.selectedItems = {};

        scope.hasItemSelected = false;
        scope.allItemsSelected = false;

        scope.toggleItemSelect = function (document) {
            scope.selectedItems[document.uuid] = !scope.selectedItems[document.uuid];
            scope.hasItemSelected = _.includes(scope.selectedItems, true);
        };

        scope.downloadMigration = function () {
            var payload = {"document": [], "all_documents": scope.allItemsSelected};
            _.forEach(scope.selectedItems, function (bool, uuid) {
                payload.document.push({parent_id: uuid});
            });

            MigrationDownload.newJob(payload, function ok() {
                console.log('posted data');

                scope.selectItems = {};
                scope.hasItemSelected = false;
                scope.allItemsSelected = false;
            }, function fail () {
                console.log('didnt post data');
            });
        };

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
        'MigrationDownloadResource',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentListController', dependencies);

})();