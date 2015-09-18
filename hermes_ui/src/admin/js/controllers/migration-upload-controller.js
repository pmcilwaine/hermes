(function () {

    var dependencies, migrationUploadController;

    migrationUploadController = function (scope, $state, $q, GenerateUrl, Upload, MigrationUploadResource) {
        var formUpload = {},
            generate_url = function () {
            var deferred = $q.defer();

            if (!_.isEmpty(formUpload)) {
                deferred.resolve(formUpload);
            } else {
                GenerateUrl.newUploadUrl().then(function ok (msg) {
                    formUpload = msg;
                    deferred.resolve(msg);
                }, function fail (msg) {
                    deferred.reject(msg);
                });
            }

            return deferred.promise;
        };

        scope.record = {};
        scope.clearFile = false;

        scope.submit = function () {
            var promises = [];
            scope.errors = {};

            if (scope.file) {

                if (scope.file[0].type !== 'application/zip' && !scope.file[0].name.match(/\.zip$/)) {
                    scope.migrationForm.file.$setValidity('file', false);
                    return false;
                }

                promises.push(generate_url().then(function ok (form) {
                    var fields = {}, file, deferred = $q.defer();

                    _.forEach(formUpload.fields, function (item) {
                        fields[item.name] = item.value;
                    });

                    scope.record.file = {
                        bucket: form.file.bucket,
                        key: form.file.key,
                        type: scope.file[0].type,
                        name: scope.file[0].name
                    };

                    file = Upload.upload({
                        url: formUpload.action,
                        method: 'POST',
                        file: scope.file[0],
                        fields: fields
                    });

                    file.progress(function () {
                    });

                    file.then(function ok (response) {
                        deferred.resolve(response);
                    }, function fail (response) {
                        deferred.reject(response);
                    });

                    return deferred.promise;
                }));

            }

            $q.all(promises).then(function ok () {
                MigrationUploadResource.post(scope.record, function ok () {
                    $state.go('document.list');
                });
            }, function fail () {
                scope.clearFile = true;
            });

        };
    };

    dependencies = [
        '$scope',
        '$state',
        '$q',
        'GenerateUrl',
        'Upload',
        'MigrationUploadResource',
        migrationUploadController
    ];

    angular.module('hermes.controllers').controller('MigrationUploadController', dependencies);

})();