(function () {

    var appController, dependencies;

    appController = function (scope) {
        scope.loading = false;
    };

    dependencies = [
        '$scope',
        appController
    ];

    angular.module('hermes.controllers').controller('AppController', dependencies);

})();