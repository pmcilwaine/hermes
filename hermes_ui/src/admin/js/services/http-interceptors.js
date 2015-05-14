(function () {

    angular.module('hermes.app').config(['$httpProvider', function (httpProvider) {

        httpProvider.interceptors.push(['$q', function ($q) {
            return {
                responseError: function (response) {
                    if (response.status === 400 && !!response.fields) {
                        return $q.reject(response);
                    }

                    return $q.reject(response);
                }
            };
        }]);

    }]);

})();