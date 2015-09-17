(function () {

    var dependencies, fileController;

    fileController = function (scope, document_list, $state, $q, document, GenerateUrl, Documents, Upload) {
        var formUpload = {};
        scope.record = document;

        scope.parent = _.reduce(_.filter(document_list, function (item) {
            return item.id === scope.record.document.parent;
        }));
        scope.document_list = document_list;

        scope.errors = {};
        scope.clearFile = false;

        var generate_url = function () {
            var deferred = $q.defer();

            if (!_.isEmpty(formUpload)) {
                console.log('already got it, resolving');
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

        scope.submit = function () {
            var promises = [];
            console.log('attempted to submit');
            scope.errors = {};

            console.log(scope.record);
            console.log(scope.file);

            if (scope.parent) {
                scope.record.document.parent = scope.parent.id;
            }

            _.each(['name', 'parent', 'url'], function (key) {
                scope.multipageForm[key].$dirty = false;
                scope.multipageForm[key].$setValidity(key, true);
            });

            if (scope.file) {

                if (scope.file[0].type !== 'application/zip') {
                    scope.multipageForm.file.$setValidity('file', false);
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
                        //console.log('progress');
                        //console.log(evt);
                    });

                    file.then(function ok (response) {
                        console.log('upload success');
                        console.log(response);
                        deferred.resolve(response);
                    }, function fail (response) {
                        console.log('upload failed');
                        console.log(response);
                        deferred.reject(response);
                    });

                    return deferred.promise;
                }));

            }

            promises.push(Documents.dryRun(scope.record));

            $q.all(promises).then(function ok () {
                Documents.save(scope.record).then(function ok () {
                    $state.go('document.list');
                }, function fail (response) {
                    if (response.fields) {
                        _.forEach(response.fields, function (value, key) {
                            scope.multipageForm[key].$dirty = true;
                            scope.multipageForm[key].$setValidity(key, false);
                            scope.errors[key] = value;
                        });
                    }
                });

            }, function fail (responses) {
                scope.clearFile = true;

                _.forEach(responses, function (response) {
                    if (response.fields) {
                        _.forEach(response.fields, function (value, key) {
                            if (scope.multipageForm[key] !== undefined) {
                                scope.multipageForm[key].$dirty = true;
                                scope.multipageForm[key].$setValidity(key, false);
                                scope.errors[key] = value;
                            }
                        });
                    }
                });
            });

        };

    };

    dependencies = [
        '$scope',
        'document_list',
        '$state',
        '$q',
        'document',
        'GenerateUrl',
        'Documents',
        'Upload',
        fileController
    ];

    angular.module('hermes.controllers').controller('MultipageFormController', dependencies);

})();