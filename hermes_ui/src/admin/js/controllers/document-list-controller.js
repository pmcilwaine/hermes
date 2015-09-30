(function () {

    var dependencies, documentController;

    documentController = function (scope, modal, DocumentList, Permissions, Documents, MigrationDownload) {
        scope.documents = DocumentList.documents;
        scope.selectedItems = {};

        scope.hasItemSelected = false;
        scope.allItemsSelected = false;
        scope.permissions = Permissions;

        scope.toggleItemSelect = function (document) {
            scope.selectedItems[document.uuid] = !scope.selectedItems[document.uuid];
            scope.hasItemSelected = _.includes(scope.selectedItems, true);
        };

        scope.downloadMigration = function () {
            MigrationDownload.options({method: 'POST'}).$promise.then(function () {
                var modalInstance = modal.open({
                    controller: 'JobModalFormController',
                    templateUrl: 'templates/views/job-name-form.html',
                    backdropClass: 'modal-backdrop h-full'
                });

                modalInstance.result.then(function (job_name) {
                    var payload = {"document": [], "all_documents": scope.allItemsSelected};
                    if (job_name) {
                        payload.name = job_name;
                    }

                    _.forEach(scope.selectedItems, function (bool, uuid) {
                        payload.document.push({parent_id: uuid});
                    });

                    MigrationDownload.newJob(payload, function ok() {
                        scope.selectItems = {};
                        scope.hasItemSelected = false;
                        scope.allItemsSelected = false;
                    }, function fail () {
                        console.log('didnt post data');
                    });
                }, function () {
                    scope.selectItems = {};
                    scope.hasItemSelected = false;
                    scope.allItemsSelected = false;
                });
            });
        };

        scope.deleteItem = function (index) {
            var record = scope.documents[index],
                modalInstance;

            if (!scope.permissions.DELETE) {
                Documents.deleteById(record.uuid);
                return;
            }

            modalInstance = modal.open({
                controller: 'DeleteController',
                templateUrl: 'templates/views/delete.html',
                backdropClass: 'modal-backdrop h-full'
            });

            modalInstance.result.then(function () {
                Documents.deleteById(record.uuid).then(function ok () {
                    scope.documents.splice(index, 1);
                }, function fail () {
                });
            });
        };
    };

    dependencies = [
        '$scope',
        '$modal',
        'DocumentList',
        'Permissions',
        'Documents',
        'MigrationDownloadResource',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentListController', dependencies);

})();