(function () {
    angular.module('hermes.app').config(['$stateProvider', '$urlRouterProvider',
        function ($stateProvider, $urlRouterProvider) {

            $urlRouterProvider.otherwise('/document/list');

            $stateProvider.state('document', {
                url: '/document',
                templateUrl: 'templates/views/document.html',
                controller: 'DocumentListController',
                resolve: {
                    DocumentList: function () { return {}; },
                    document: function () { return {}; }
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
                        return Documents.getAll();
                    }]
                },
                data: {
                    tab: true
                }
            });

            $stateProvider.state('document.add', {
                url: '/add',
                templateUrl: 'templates/views/document-form.html',
                controller: 'DocumentFormController',
                resolve: {
                    document: function () { return {}; }
                }
            });

            $stateProvider.state('document.page', {
                url: '/page/:id',
                templateUrl: 'templates/views/page-form.html',
                controller: 'PageFormController',
                resolve: {
                    document: ['Documents', 'DocumentResource', '$stateParams',
                        function (Documents, DocumentResource, stateParams) {
                            if (stateParams.id) {
                                return Documents.getDocument(stateParams.id);
                            } else {
                                return Documents.getNewDocument();
                            }
                        }]
                }
            });

            $stateProvider.state('document.file', {
                'url': '/file/:id',
                templateUrl: 'templates/views/file-form.html',
                controller: 'FileFormController',
                resolve: {
                    document: ['Documents', 'DocumentResource', '$stateParams',
                        function (Documents, DocumentResource, stateParams) {
                            console.log(stateParams);
                            return Documents.getNewDocument();
                        }]
                }
            });

            $stateProvider.state('document.multipage', {
                'url': '/multipage/:id',
                templateUrl: 'templates/views/multipage-form.html',
                controller: 'MultipageFormController',
                resolve: {
                    document: ['Documents', 'DocumentResource', '$stateParams',
                        function (Documents, DocumentResource, stateParams) {
                            console.log(stateParams);
                            return Documents.getNewDocument();
                        }]
                }
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
                url: '/modify/{id:int}',
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