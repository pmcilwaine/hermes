(function () {

    var dependencies, userController;

    userController = function (scope, userList, Users) {
        scope.users = userList;

        scope.deleteItem = function (index) {
            var record = scope.users[index];
            Users.deleteById(record.uid).then(function ok (response) {
                scope.users.splice(index, 1);
            }, function fail (response) {
            });
        };
    };

    dependencies = [
        '$scope',
        'UserList',
        'Users',
        userController
    ];

    angular.module('hermes.controllers').controller('UserListController', dependencies);

})();