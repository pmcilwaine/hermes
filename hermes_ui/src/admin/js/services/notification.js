(function () {

    var notificationService, dependencies;

    notificationService = function (rootScope) {
        var service = {}, items = [];

        service.addNotification = function (msg_obj) {
            items.push(msg_obj);
            rootScope.$broadcast('hermes_notification_new', msg_obj);
        };

        service.getNotification = function () {
            return _.last(items);
        };

        service.clear = function () {
            items = [];
        };

        return service;
    };

    dependencies = [
        '$rootScope',
        notificationService
    ];

    angular.module('hermes.services').factory('Notification', dependencies);

})();