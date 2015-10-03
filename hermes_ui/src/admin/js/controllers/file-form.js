(function () {

    var dependencies, fileController;

    fileController = function (scope, document_list, $state, $q, document, GenerateUrl, Documents, Upload) {
        var formUpload = {},
            rewriteUrl = function () {
                var url = _.snakeCase(scope.record.document.name).replace(/_/g, '-');
                if (scope.parent.url) {
                    scope.record.document.url = scope.parent.url + '/' + url;
                } else {
                    scope.record.document.url = url;
                }
            };

        scope.record = document;
        scope.savingForm = false;
        scope.progressPercentage = 0;

        scope.parent = _.reduce(_.filter(document_list, function (item) {
            return item.id === scope.record.document.parent;
        }));
        scope.document_list = document_list;

        scope.errors = {};
        scope.clearFile = false;

        scope.$watch('parent', function (item) {
            if (!!item && item.url) {
                rewriteUrl();
            } else if (item && item.id === 0) {
                rewriteUrl();
            }
        });

        var generate_url = function () {
            var deferred = $q.defer();

            if (!_.isEmpty(formUpload)) {
                console.log('already got it, resolving');
                deferred.resolve(formUpload);
            } else {
                GenerateUrl.newUploadUrl().then(function ok (msg) {
                    console.log('got new url, resolved');
                    formUpload = msg;
                    deferred.resolve(msg);
                }, function fail (msg) {
                    console.log('failed to get new url');
                    deferred.reject(msg);
                });
            }

            return deferred.promise;
        };

        scope.submit = function () {
            var promises = [];
            console.log('attempted to submit');
            scope.errors = {};
            scope.savingForm = true;

            console.log(scope.record);
            console.log(scope.file);

            if (scope.parent) {
                scope.record.document.parent = scope.parent.id;
            }

            _.each(['name', 'parent', 'url'], function (key) {
                scope.fileForm[key].$dirty = false;
                scope.fileForm[key].$setValidity(key, true);
            });

            if (scope.file) {

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

                    file.progress(function (evt) {
                        scope.progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
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
                    scope.savingForm = false;
                    $state.go('document.list');
                }, function fail (response) {
                    scope.savingForm = false;
                    scope.progressPercentage = 0;
                    if (response.fields) {
                        _.forEach(response.fields, function (value, key) {
                            scope.fileForm[key].$dirty = true;
                            scope.fileForm[key].$setValidity(key, false);
                            scope.errors[key] = value;
                        });
                    }
                });

            }, function fail (responses) {
                scope.clearFile = true;
                scope.savingForm = false;
                scope.progressPercentage = 0;

                _.forEach(responses, function (response) {
                   if (response.fields) {
                       _.forEach(response.fields, function (value, key) {
                           scope.fileForm[key].$dirty = true;
                           scope.fileForm[key].$setValidity(key, false);
                           scope.errors[key] = value;
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

    angular.module('hermes.controllers').controller('FileFormController', dependencies);

})();