(function () {

    var dependencies, userController;

    userController = function (scope, userList, RestoreUserResource) {
        scope.users = userList;

        scope.restoreItem = function (index) {
            var record = scope.users[index];
            scope.users.splice(index, 1);
            RestoreUserResource.put(record, function ok () {
            }, function fail () {
            });
        };
    };

    dependencies = [
        '$scope',
        'UserList',
        'RestoreUserResource',
        userController
    ];

    angular.module('hermes.controllers').controller('RestoreUserListController', dependencies);

})();