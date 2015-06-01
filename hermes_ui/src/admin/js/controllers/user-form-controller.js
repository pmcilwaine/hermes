(function () {

    var dependencies, userFormController;

    userFormController = function (scope, state, user, Users) {
        scope.record = user;
        scope.action = user.is_new !== undefined ? "Add User" : "Modify User";
        scope.errors = {};

        scope.submit = function () {
            Users.save(scope.record).then(function save () {
                state.go('users.list');
            }, function failed(msg) {
                _.each(msg.data.fields, function (value, key) {
                    scope.userForm[key].$dirty = true;
                    scope.userForm[key].$setValidity(key, false);
                    scope.errors[key] = value;
                });
            });
        };
    };

    dependencies = [
        '$scope',
        '$state',
        'user',
        'Users',
        userFormController
    ];

    angular.module('hermes.controllers').controller('UserFormController', dependencies);

})();