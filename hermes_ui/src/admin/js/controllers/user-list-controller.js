(function () {

    var dependencies, userController;

    userController = function (scope, modal, userList, Permissions, Users) {
        scope.users = userList;
        scope.permissions = Permissions;

        scope.deleteItem = function (index) {
            var record = scope.users[index],
                modalInstance;

            if (!scope.permissions.DELETE) {
                Users.deleteById(record.id);
                return;
            }

            modalInstance = modal.open({
                controller: 'DeleteController',
                templateUrl: 'templates/views/delete.html',
                backdropClass: 'modal-backdrop h-full'
            });

            modalInstance.result.then(function () {
                Users.deleteById(record.id).then(function ok () {
                    scope.users.splice(index, 1);
                }, function fail () {
                });
            });
        };
    };

    dependencies = [
        '$scope',
        '$modal',
        'UserList',
        'Permissions',
        'Users',
        userController
    ];

    angular.module('hermes.controllers').controller('UserListController', dependencies);

})();