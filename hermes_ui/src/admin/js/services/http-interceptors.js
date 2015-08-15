(function () {

    angular.module('hermes.app').config(['$httpProvider', function (httpProvider) {

        httpProvider.interceptors.push(['$q', 'Notification', function ($q, Notification) {
            return {
                responseError: function (response) {
                    if (response.data.notify_msg) {
                        Notification.addNotification(response.data.notify_msg, response.status);
                    }
                    return $q.reject(response);
                },
                response: function (response) {
                    if (response.data.notify_msg) {
                        Notification.addNotification(response.data.notify_msg, response.status);
                    }
                    return response;
                }
            };
        }]);

    }]);

})();