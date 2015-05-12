(function () {

    var dependencies, userController;

    userController = function (scope, userList, Users) {
        scope.users = userList;

        scope.deleteItem = function (index) {
            var record = scope.users[index];
            Users.deleteById(record.uid).then(function ok (response) {
                scope.users.splice(index, 1);
                console.log('ok');
                console.log(response);
            }, function fail (response) {
                console.log('fail');
                console.log(response);
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