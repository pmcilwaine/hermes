(function () {

    var alertService, dependencies;

    alertService = function () {
        var service = {}, data = [];

        service.add = function (state, message) {
            data.push({
                state: state,
                message: message
            });
        };

        service.get = function () {
            return data.pop();
        };

        return service;
    };

    dependencies = [
        alertService
    ];

    angular.module('hermes.services').factory('Alert', dependencies);

})();