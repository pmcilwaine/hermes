(function () {
    angular.module('hermes.app').config(['$stateProvider', '$urlRouterProvider',
        function ($stateProvider, $urlRouterProvider) {

            $urlRouterProvider.otherwise('/document');

            $stateProvider.state('document', {
                url: '/document',
                templateUrl: 'templates/views/document.html',
                controller: 'DocumentListController',
                data: {
                    tab: true,
                    label: 'Documents'
                }
            });

            $stateProvider.state('users', {
                url: '/user',
                templateUrl: 'templates/views/user.html',
                controller: 'UserListController',
                data: {
                    tab: true,
                    label: 'Users'
                }
            });

            $stateProvider.state('jobs', {
                url: '/job',
                templateUrl: 'templates/views/job.html',
                controller: 'JobListController',
                data: {
                    tab: true,
                    label: 'Jobs'
                }
            });

            $stateProvider.state('analytics', {
                url: '/analytics',
                templateUrl: 'templates/views/analytics.html',
                controller: 'AnalyticsController',
                data: {
                    tab: true,
                    label: 'Analytics'
                }
            });

        }]);
})();