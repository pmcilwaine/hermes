(function () {

    var dependencies, documentController;

    documentController = function (scope, $state, Documents) {
        scope.record = {
            document: {}
        };

        scope.errors = {};

        // TODO this should be pulled in from Configuration Registry
        scope.documentTypes = [
            'Page',
            'File',
            'MultiPage'
        ];

        // TODO this should be pulled in from Configuration Registry
        scope.pageTemplates = [
            'Homepage',
            'Standard'
        ];

        scope.submit = function () {
            // TODO do document validation
            scope.errors = {};
            console.log('the documentForm');
            console.log(scope.documentForm);

            _.each(['name', 'type', 'parent', 'url'], function (key) {
                scope.documentForm[key].$dirty = false;
                scope.documentForm[key].$setValidity(key, true);
            });

            console.log('before go');
            console.log(scope.record);
            Documents.dryRun(scope.record).$promise.then(function ok (msg) {
                Documents.createNewDocument(scope.record);
                $state.go('document.page');
            }, function fail (msg) {
                console.log('errors');
                console.log(msg);

                _.each(msg.data.fields, function (value, key) {
                    scope.documentForm[key].$dirty = true;
                    scope.documentForm[key].$setValidity(key, false);
                    scope.errors[key] = value;
                });
            });
        };
    };

    dependencies = [
        '$scope',
        '$state',
        'Documents',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentFormController', dependencies);

})();
