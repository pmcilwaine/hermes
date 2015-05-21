(function () {

    angular.module('hermes.services', ['ngResource'])
        .factory('UserResource', ['$resource', function (resource) {
            return resource('/admin/user/:id', {id: '@user_id'}, {
                get: {method: 'GET'},
                post: {method: 'POST'},
                put: {method: 'PUT'},
                delete: {method: 'DELETE'}
            });
        }])
        .factory('DocumentResource', ['$resource', function (resource) {
            return resource('/admin/document/:id', {id: '@id'}, {
                get: {method: 'GET'},
                post: {method: 'POST'},
                put: {method: 'PUT'},
                delete: {method: 'DELETE'},
                dryRun: {method: 'POST', params: {validate: true}}
            });
        }])
        .factory('UploadUrlResource', ['$resource', function (resource) {
            return resource('/admin/upload_url', {}, {
                post: {method: 'POST'}
            });
        }]);

})();