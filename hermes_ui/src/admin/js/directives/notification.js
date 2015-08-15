(function () {

    var dependencies, notificationDirective;

    notificationDirective = function (rootScope, Notification) {

        return {
            scope: {},
            templateUrl: 'templates/directives/notification.html',
            link: {},
            controller: ['$scope', function ($scope) {
                var _notification = Notification.getNotification();
                function defaultState() {
                    $scope.message = $scope.title = null;
                    $scope.stateDanger = false;
                    $scope.stateSuccess = false;
                    $scope.closed = true;
                }

                function showNotification(notification) {
                    $scope.message = notification.message;
                    $scope.title = notification.title;

                    if (notification.type === 'error') {
                        $scope.stateDanger = true;
                    } else {
                        $scope.stateSuccess = true;
                    }

                    $scope.closed = false;
                    // Notification.clear();
                }

                rootScope.$on('hermes_notification_new', function (name, notification) {
                    showNotification(notification);
                });

                $scope.close = function () {
                    defaultState();
                    Notification.clear();
                };

                defaultState();
                if (_notification) {
                    showNotification(_notification);
                }
            }]
        };
    };

    dependencies = [
        '$rootScope',
        'Notification',
        notificationDirective
    ];

    angular.module('hermes.directives').directive('hermesNotification', dependencies);

})();