(function () {
    angular.module('hermes.app').config(['$stateProvider', '$urlRouterProvider',
        function ($stateProvider, $urlRouterProvider) {

            $urlRouterProvider.otherwise('/document');

            $stateProvider.state('document', {
                url: '/document',
                templateUrl: 'templates/views/document.html',
                controller: 'DocumentListController',
                resolve: {
                    DocumentList: function () { return {}; }
                },
                data: {
                    tab: false,
                    label: 'Documents'
                }
            });

            $stateProvider.state('document.list', {
                url: '/list',
                templateUrl: 'templates/views/document-list.html',
                controller: 'DocumentListController',
                resolve: {
                    DocumentList: ['Documents', function (Documents) {
                        return Documents.get();
                    }]
                },
                data: {
                    tab: true
                }
            });

            $stateProvider.state('document.add', {
                url: '/add',
                templateUrl: 'templates/views/document-form.html',
                controller: 'DocumentFormController'
            });

            $stateProvider.state('users', {
                abstract: true,
                url: '/user',
                templateUrl: 'templates/views/user.html',
                controller: 'UserController',
                data: {
                    tab: false,
                    label: 'Users'
                },
                resolve: {
                    UserList: function () { return {}; },
                    user: function () { return {}; }
                }
            });

            $stateProvider.state('users.list', {
                url: '/list',
                templateUrl: 'templates/views/user-list.html',
                controller: 'UserListController',
                resolve: {
                    UserList: ['Users', function (Users) {
                        return Users.getAll();
                    }]
                },
                data: {
                    tab: true
                }
            });

            $stateProvider.state('users.add', {
                url: '/add',
                templateUrl: 'templates/views/user-form.html',
                controller: 'UserFormController',
                data: {
                    tab: false
                },
                resolve: {
                    user: ['Users', function (Users) {
                        return Users.createNew();
                    }]
                }
            });

            $stateProvider.state('users.modify', {
                url: '/modify/:id',
                templateUrl: 'templates/views/user-form.html',
                controller: 'UserFormController',
                data: {
                    tab: false
                },
                resolve: {
                    user: ['Users', '$stateParams', function (Users, params) {
                        return Users.getById(params.id);
                    }]
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