(function () {

    var dependencies, userService;

    userService = function ($q, UserResource) {
        var user = {}, data = [];

        user.createNew = function () {
            return {is_new: true};
        };

        user.save = function (record) {
            var deferred = $q.defer();

            if (record.is_new || record.id === undefined) {
                UserResource.post(record, function ok (msg) {
                    deferred.resolve(msg);
                }, function fail (msg) {
                    deferred.reject(msg);
                });
            } else {
                UserResource.put(record, function ok (msg) {
                    deferred.resolve(msg);
                }, function fail (msg) {
                    deferred.reject(msg);
                });
            }

            return deferred.promise;
        };

        user.getById = function (user_id) {
            console.log('get by id');
            var deferred = $q.defer();
            UserResource.get({id: user_id}, function ok (response) {
                deferred.resolve(response);
            }, function fail (response) {
                console.log('rejected getting user');
                deferred.reject(response);
            });

            return deferred.promise;
        };

        user.deleteById = function (user_id) {
            var deferred = $q.defer();
            UserResource.delete({id: user_id}, function ok (msg) {
                deferred.resolve(msg);
            }, function fail (msg) {
                deferred.reject(msg);
            });

            return deferred.promise;
        };

        user.getAll = function () {
            return UserResource.get().$promise.then(function (users) {
                data = users.users;
                return data;
            });
        };

        user.hasPermission = function (method) {
            var deferred = $q.defer();
            UserResource.options({method: method}).$promise.then(function ok (response) {
                if (response[method]) {
                    deferred.resolve(response);
                } else {
                    deferred.reject(response);
                }
            });

            return deferred.promise;
        };

        return user;
    };

    dependencies = [
        '$q',
        'UserResource',
        userService
    ];

    angular.module('hermes.services').factory('Users', dependencies);

})();