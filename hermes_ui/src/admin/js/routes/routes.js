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

            $stateProvider.state('document.restore', {
                url: '/restore',
                templateUrl: 'templates/views/document-restore-list.html',
                controller: 'DocumentRestoreController',
                resolve: {
                    DocumentList: ['Documents', function (Documents) {
                        return Documents.getAllRestore();
                    }]
                }
            });

            $stateProvider.state('document.add', {
                url: '/add',
                templateUrl: 'templates/views/document-form.html',
                controller: 'DocumentFormController',
                resolve: {
                    document: function () { return {}; },
                    document_list: ['Documents', function (Documents) {
                        return Documents.getAllWithRepeat(String.fromCharCode(160));
                    }],
                    option: ['Documents', function (Documents) {
                        return Documents.hasPermission('POST');
                    }]
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
                        }],
                    document_list: ['Documents', function (Documents) {
                        return Documents.getAllWithRepeat(String.fromCharCode(160));
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
                            if (stateParams.id) {
                                return Documents.getDocument(stateParams.id);
                            } else {
                                return Documents.getNewDocument();
                            }
                        }],
                    document_list: ['Documents', function (Documents) {
                        return Documents.getAllWithRepeat(String.fromCharCode(160));
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
                            if (stateParams.id) {
                                return Documents.getDocument(stateParams.id);
                            } else {
                                return Documents.getNewDocument();
                            }
                        }],
                    document_list: ['Documents', function (Documents) {
                        return Documents.getAllWithRepeat(String.fromCharCode(160));
                    }]
                }
            });

            $stateProvider.state('document.migration', {
                url: '/migration',
                templateUrl: 'templates/views/migration-upload.html',
                controller: 'MigrationUploadController',
                resolve: {
                    option: ['MigrationUploadResource', '$q', function (MigrationUploadResource, $q) {
                        var deferred = $q.defer();
                        MigrationUploadResource.options({method: 'POST'}).$promise.then(function () {
                            deferred.resolve(true)
                        }, function () {
                            deferred.reject(false)
                        });

                        return deferred.promise;
                    }]
                }
            });

            $stateProvider.state('document.versions', {
                url: '/version/{id:int}',
                controller: 'RestoreDocumentVersionController',
                templateUrl: 'templates/views/document-restore-version-list.html',
                resolve: {
                    DocumentList: ['Documents', '$stateParams', function (Documents, stateParams) {
                        return Documents.listVersions(stateParams.id);
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

            $stateProvider.state('users.restore', {
                url: '/restore',
                templateUrl: 'templates/views/restore-user-list.html',
                controller: 'RestoreUserListController',
                resolve: {
                    UserList: ['RestoreUserResource', function (RestoreUserResource) {
                        return RestoreUserResource.get().$promise.then(function (data) {
                            return data.users;
                        });
                    }]
                },
                data: {
                    tab: false
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
                    }],
                    option: ['Users', function (Users) {
                        return Users.hasPermission('POST');
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