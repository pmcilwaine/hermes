(function () {

    var dependencies, pageController;

    pageController = function (scope, $state, document, Documents) {
        console.log('in page controller');

        console.log('document');
        console.log(document);
        scope.record = document;

        // TODO this should be pulled in from Configuration Registry
        scope.pageTemplates = [
            'Homepage',
            'Standard'
        ];

        scope.submit = function () {
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
        '$state',
        'document',
        'Documents',
        pageController
    ];

    angular.module('hermes.controllers').controller('PageFormController', dependencies);

})();