(function () {

    angular.module('hermes.services', ['ngResource'])
        .factory('UserResource', ['$resource', function (resource) {
            return resource('/admin/user/:id', {id: '@id'}, {
                get: {method: 'GET'},
                post: {method: 'POST'},
                put: {method: 'PUT'},
                delete: {method: 'DELETE'}
            });
        }])
        .factory('DocumentResource', ['$resource', function (resource) {
            return resource('/admin/document/:id', {id: '@uuid'}, {
                get: {method: 'GET'},
                post: {method: 'POST'},
                put: {method: 'PUT', params: {id: '@id'}},
                delete: {method: 'DELETE'},
                dryRun: {method: 'POST', params: {validate: true}}
            });
        }])
        .factory('UploadUrlResource', ['$resource', function (resource) {
            return resource('/admin/upload_url', {}, {
                post: {method: 'POST'}
            });
        }])
        .factory('DownloadUrlResource', ['$resource', function (resource) {
            return resource('/admin/download_url', {}, {
                post: {method: 'POST'}
            });
        }])
        .factory('JobResource', ['$resource', function (resource) {
            return resource('/admin/job', {}, {
                get: {method: 'GET'}
            });
        }])
        .factory('MigrationUploadResource', ['$resource', function (resource) {
            return resource('/admin/migration_upload', {}, {
                post: {method: 'POST'}
            });
        }])
        .factory('MigrationDownloadResource', ['$resource', function (resource) {
            return resource('/admin/migration', {}, {
                newJob: {method: 'post'}
            });
        }])
        .factory('RestoreUserResource', ['$resource', function (resource) {
            return resource('/admin/restore_user/:id', {id: '@id'}, {
                put: {method: 'PUT'}
            });
        }])
        .factory('RestoreDocumentResource', ['$resource', function (resource) {
            return resource('/admin/restore_document/:id', {id: '@uuid'}, {
                put: {method: 'PUT'}
            });
        }]);

})();