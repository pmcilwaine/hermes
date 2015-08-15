(function () {

    var dependencies, jobController;

    jobController = function (scope, $modalInstance) {

        scope.ok = function () {
            $modalInstance.close(scope.name);
        };

        scope.cancel = function () {
            $modalInstance.dismiss('cancel');
        };

    };

    dependencies = [
        '$scope',
        '$modalInstance',
        jobController
    ];

    angular.module('hermes.controllers').controller('JobModalFormController', dependencies);

})();
