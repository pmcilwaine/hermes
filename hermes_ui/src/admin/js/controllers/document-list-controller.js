(function () {

    var dependencies, documentController;

    documentController = function (scope, DocumentList) {
        scope.documents = DocumentList.documents;
    };

    dependencies = [
        '$scope',
        'DocumentList',
        documentController
    ];

    angular.module('hermes.controllers').controller('DocumentListController', dependencies);

})();