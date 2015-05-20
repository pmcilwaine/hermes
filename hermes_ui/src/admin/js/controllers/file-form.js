(function () {

    var dependencies, fileController;

    fileController = function (scope, $state, $q, document, GenerateUrl, Documents, Upload) {
        scope.record = document;
        scope.errors = {};

        GenerateUrl.newUploadUrl().then(function ok (msg) {
           console.log(msg);
        }, function fail (msg) {

        });

        /*
        scope.uploader = new FileUploader({
            method: 'PUT',
            headers: {
                'Content-Type': 'application/octet-stream'
            }
        });*/

        /*
        GenerateUrl.newUploadUrl().then(function ok (msg) {
            console.log('ok');
            console.log(msg);
            scope.uploader.url = msg.upload_url;
        }, function fail (msg) {
            console.log('fail');
            console.log(msg);
        });*/

        scope.submit = function () {
            console.log('attempted to submit');
            scope.errors = {};

            console.log(scope.record);

            console.log(scope.file);

            if (scope.file) {
                console.log('yes');
                Upload.upload({
                    url: '',
                    method: 'POST'
                })
            }

            _.each(['name', 'parent', 'url'], function (key) {
                scope.fileForm[key].$dirty = false;
                scope.fileForm[key].$setValidity(key, true);
            });

            /*
            var queue = _.first(scope.uploader.queue);
            if (queue) {
                queue.onComplete(function (response, status, headers) {
                    console.log('onComplete');
                    console.log(response);
                    console.log(status);
                    console.log(headers);
                });
                queue.upload();
            }*/

            /*
            promises.push(GenerateUrl.newUploadUrl());
            promises.push(Documents.dryRun(scope.record));

            $q.all(promises).then(function ok (msg) {
                console.log('all.promises ok');
                console.log(msg);
            }, function fail (msg) {
                console.log('all.promises fail');
                console.log(msg);
            });*/

            /*scope.uploader.upload(function () {

            });*/

            /*
            Documents.save(scope.record).$promise.then(function ok (msg) {
                console.log('ok');
                console.log(msg);
                $state.go('document.list');
            }, function fail (msg) {
                console.log('failed');
                console.log(msg);

                _.each(msg.data.fields, function (value, key) {
                    if (scope.fileForm[key] !== undefined) {
                        scope.fileForm[key].$dirty = true;
                        scope.fileForm[key].$setValidity(key, false);
                        scope.errors[key] = value;
                    }
                });
            });*/
        };

    };

    dependencies = [
        '$scope',
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