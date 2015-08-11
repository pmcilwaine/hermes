(function () {

    var dependencies, userController;

    userController = function (scope, $state, userList, RestoreUserResource) {
        scope.users = userList;

        scope.restoreItem = function (index) {
            var record = scope.users[index];
            RestoreUserResource.put(record, function ok () {
                $state.go('users.list');
            }, function fail () {
            });
        };
    };

    dependencies = [
        '$scope',
        '$state',
        'UserList',
        'RestoreUserResource',
        userController
    ];

    angular.module('hermes.controllers').controller('RestoreUserListController', dependencies);

})();