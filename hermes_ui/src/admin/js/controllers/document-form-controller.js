(function () {

    var dependencies, documentController;

    documentController = function (scope, document_list, $state, Documents) {
        var rewriteUrl = function () {
            var url = _.snakeCase(scope.record.document.name).replace(/_/g, '-');
            if (scope.parent.url) {
                scope.record.document.url = scope.parent.url + '/' + url;
            } else {
                scope.record.document.url = url;
            }
        };

        scope.record = {
            document: {
                type: 'Page',
                url: undefined
            },
            page: {
                template: 'Standard'
            }
        };

        scope.parent = 0;
        scope.document_list = document_list;

        scope.errors = {};

        // TODO this should be pulled in from Configuration Registry
        scope.documentTypes = [
            'Page',
            'File',
            'MultiPage'
        ];

        // TODO this should be pulled in from Configuration Registry
        scope.pageTemplates = [
            /*'Homepage',*/
            'Standard'
        ];

        scope.submit = function () {
            // TODO do document validation
            scope.errors = {};

            if (scope.parent) {
                scope.record.document.parent = scope.parent.id;
            }

            _.each(['name', 'type', 'parent', 'url'], function (key) {
                scope.documentForm[key].$dirty = false;
                scope.documentForm[key].$setValidity(key, true);
            });

            Documents.dryRun(scope.record).then(function ok () {
                Documents.createNewDocument(scope.record);
                $state.go('document.' + scope.record.document.type.toLowerCase());
            }, function fail (msg) {
                _.each(msg.fields, function (value, key) {
                    scope.documentForm[key].$dirty = true;
                    scope.documentForm[key].$setValidity(key, false);
                    scope.errors[key] = value;
                });
            });
        };

        scope.$watch('parent', function (item) {
            if (!!item && item.url) {
                rewriteUrl();
            }
        });

        scope.$watch('record.document.name', function (name) {
            if (name) {
                rewriteUrl();
            }
        });
    };

    dependencies = [
        '$scope',
        'document_list',
        '$state',
        'Documents',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentFormController', dependencies);

})();
