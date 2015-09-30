(function () {

    var dependencies, userController;

    userController = function (scope, modal, userList, Users) {
        scope.users = userList;

        scope.deleteItem = function (index) {
            var modalInstance = modal.open({
                controller: 'DeleteController',
                templateUrl: 'templates/views/delete.html',
                backdropClass: 'modal-backdrop h-full'
            }),
                record = scope.users[index];

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
        'Users',
        userController
    ];

    angular.module('hermes.controllers').controller('UserListController', dependencies);

})();