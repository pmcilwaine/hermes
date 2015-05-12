(function () {

    var dependencies, userService;

    userService = function ($q, UserResource) {
        var user = {}, data = [];

        user.createNew = function () {
            return {is_new: true};
        };

        user.save = function (record) {
            var deferred = $q.defer();

            if (record.is_new || record.user_id === undefined) {
                UserResource.post(record, function ok (msg) {
                    console.log('ok post');
                    console.log(msg);
                    deferred.resolve(msg);
                }, function fail (msg) {
                    console.log('fail post');
                    console.log(msg);
                    deferred.reject(msg);
                });
            } else {
                UserResource.put(record, function ok (msg) {
                    console.log('ok put');
                    console.log(msg);
                    deferred.resolve(msg);
                }, function fail (msg) {
                    console.log('fail put');
                    console.log(msg);
                    deferred.reject(msg);
                });
            }

            return deferred.promise;
        };

        user.getById = function (user_id) {
            var t = _.findWhere(data, {uid: user_id});
            console.log(t);
            return t;
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
            console.log('getAll');
            return UserResource.get().$promise.then(function (users) {
                data = users.users;
                return data;
            });
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