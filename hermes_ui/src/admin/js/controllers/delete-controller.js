(function () {

    var dependencies, deleteController;

    deleteController = function (scope, $modalInstance) {

        scope.ok = function () {
            $modalInstance.close();
        };

        scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };

    };

    dependencies = [
        '$scope',
        '$modalInstance',
        deleteController
    ];

    angular.module('hermes.controllers').controller('DeleteController', dependencies);

})();
