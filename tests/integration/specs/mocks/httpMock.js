module.exports = {
    register: function () {

        var mock = function () {
            angular.module('hermes.httpmock', ['hermes.app', 'ngMockE2E']).run(function($httpBackend) {

                var users = [{
                    id: 1,
                    email: 'test@example.org',
                    first_name: 'Test',
                    last_name: 'User'
                }], documents = [{
                    name: 'Homepage',
                    url: 'index',
                    path: '1/',
                    id: 1
                }], uuid = function () {
                    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                        var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
                        return v.toString(16);
                    });
                };

                $httpBackend.whenGET('/admin/user').respond({
                    users: users
                });

                $httpBackend.whenGET('/admin/user/1').respond(users[0]);

                $httpBackend.whenPUT('/admin/user/1').respond(function (method, url, data) {
                    data = angular.fromJson(data);
                    users.forEach(function (item) {
                        if (item.email === data.email) {
                            item.first_name = data.first_name;
                        }
                    })
                    return [200, data, {}];
                });

                $httpBackend.whenPOST('/admin/user').respond(function (method, url, data) {
                    data = angular.fromJson(data);
                    data.id = users.length;
                    users.push(data);
                    return [200, data, {}];
                });

                $httpBackend.whenDELETE(/\/admin\/user\/.*?$/).respond(function (method, url, data) {
                    var user_id = url.split('/')[3];

                    users = users.filter(function (item) {
                        return item.id !== user_id;
                    });

                    return [200, data, {}];
                });

                $httpBackend.whenGET('/admin/document?limit=100&offset=0').respond({
                    documents: documents
                });

                $httpBackend.whenPOST('/admin/document?validate=true', function (data) {
                    data = angular.fromJson(data);
                    return ['first-document', 'first-file'].indexOf(data.document.url) !== -1;
                }).respond(function (method, url, data) {
                    return [200, {}, {}];
                });

                $httpBackend.whenPOST('/admin/document?validate=true', function (data) {
                    data = angular.fromJson(data);
                    return ['fail-document'].indexOf(data.document.url) !== -1;
                }).respond(function (method, url, data) {
                    return [400, {fields: {
                        url: 'URL is already in use'
                    }}, {}];
                });

                $httpBackend.whenPOST('/admin/document?validate=true', function (data) {
                    data = angular.fromJson(data);
                    return data.document.url === undefined;
                }).respond(function (method, url, data) {
                    return [400, {fields: {
                        name: 'Must enter a name',
                        url: 'URL is already in use',
                        type: 'Must select a type'
                    }}, {}];
                });

                $httpBackend.whenPOST('/admin/document', function (data) {
                    data = angular.fromJson(data);
                    return ['first-document', 'first-file'].indexOf(data.document.url) !== -1 && data.document.url !== '';
                }).respond(function (method, url, data) {
                    data = angular.fromJson(data);
                    data.document.id = documents.length;
                    data.document.path = data.document.id + '/';
                    documents.push(data.document);
                    return [200, data.document, {}];
                });

                $httpBackend.whenPOST('/admin/file/upload').respond({});

                $httpBackend.whenPOST('/admin/upload_url').respond({
                    fields: [{
                        bucket: null
                    }],
                    action: '/admin/file/upload'
                });

                $httpBackend.when('OPTIONS', /.*/).passThrough();
            });
        };

        browser.addMockModule('hermes.httpmock', mock);
    }
};