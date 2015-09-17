(function () {

    var dependencies, userFormController;

    userFormController = function (scope, state, user, Users) {
        scope.record = user;
        scope.action = user.is_new !== undefined ? "Add User" : "Modify User";
        scope.errors = {};
        scope.user_permissions = {};

        scope.permissions = [
            {value: 'list_document', title: 'List Documents'},
            {value: 'add_document', title: 'Add Document'},
            {value: 'modify_document', title: 'Modify Document'},
            {value: 'delete_document', title: 'Delete Document'},
            {value: 'restore_deleted_document', title: 'Restore Deleted Document'},
            {value: 'restore_version_document', title: 'Restore Version Document'},
            {value: 'download_archive_document', title: 'Download Migration Archive'},
            {value: 'upload_archive_document', title: 'Upload Migration Archive'},
            {value: 'list_job', title: 'List Job'},
            {value: 'list_user', title: 'List User'},
            {value: 'add_user', title: 'Add User'},
            {value: 'modify_user', title: 'Modify User'},
            {value: 'delete_user', title: 'Delete User'},
            {value: 'restore_user', title: 'Restore User'}
        ];

        _.each(scope.permissions, function (permission) {
            scope.user_permissions[permission.value] = !!_.find(scope.record.permissions, function (item) {
                return item === permission.value;
            });
        });

        scope.is_administrator = _.all(scope.user_permissions);

        scope.togglePermissions = function () {
            _.each(scope.user_permissions, function (value, key) {
                scope.user_permissions[key] = scope.is_administrator;
            });
        };

        scope.checkAdmin = function () {
            scope.is_administrator = _.all(scope.user_permissions);
        }

        scope.submit = function () {
            // update scope.record
            scope.record.permissions = [];
            _.each(scope.user_permissions, function (value, key) {
                if (value) {
                    scope.record.permissions.push(key);
                }
            });

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