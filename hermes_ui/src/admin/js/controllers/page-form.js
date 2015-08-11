(function () {

    var dependencies, pageController;

    pageController = function (scope, document_list, $state, document, Documents) {
        scope.record = document;

        scope.parent = _.reduce(_.filter(document_list, function (item) {
            return item.id === scope.record.document.parent;
        }));
        scope.document_list = document_list;
        // TODO this should be pulled in from Configuration Registry
        scope.pageTemplates = [
            'Homepage',
            'Standard'
        ];

        scope.submit = function () {
            if (scope.parent) {
                scope.record.document.parent = scope.parent.id;
            }

            console.log('attempted to submit');
            Documents.save(scope.record).then(function ok (msg) {
                console.log('ok');
                console.log(msg);
                $state.go('document.list');
            }, function fail (msg) {
               console.log('failed');
                console.log(msg);
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