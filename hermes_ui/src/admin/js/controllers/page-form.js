(function () {

    var dependencies, pageController;

    pageController = function (scope, document_list, $state, document, Documents) {
        scope.record = document;
        scope.savingForm = false;
        scope.errors = {};

        if (!scope.record.document) {
            $state.go('document.add');
            return;
        }

        scope.parent = _.reduce(_.filter(document_list, function (item) {
            return item.id === scope.record.document.parent;
        }));
        scope.document_list = document_list;
        // TODO this should be pulled in from Configuration Registry
        scope.pageTemplates = [
            'Standard'
        ];

        scope.submit = function () {
            if (scope.parent) {
                scope.record.document.parent = scope.parent.id;
            }

            scope.savingForm = true;
            Documents.save(scope.record).then(function ok () {
                $state.go('document.list');
            }, function fail (msg) {
                _.each(msg.data.fields, function (value, key) {
                    scope.pageForm[key].$dirty = true;
                    scope.pageForm[key].$setValidity(key, false);
                    scope.errors[key] = value;
                });
                scope.savingForm = false;
            });
        };

    };

    dependencies = [
        '$scope',
        'document_list',
        '$state',
        'document',
        'Documents',
        pageController
    ];

    angular.module('hermes.controllers').controller('PageFormController', dependencies);

})();