(function () {

    angular.module('hermes.app').config(['$httpProvider', function (httpProvider) {

        httpProvider.interceptors.push(['$q', function ($q) {
            return {
                responseError: function (response) {
                    console.log('responseError');
                    console.log(response);
                    if (response.status === 400 && !!response.fields) {
                        console.log('reject and show custom message this is a test');
                        return $q.reject(response);
                    }

                    console.log('pass thru as fail');
                    return $q.reject(response);
                }
            };
        }]);

    }]);

    angular.module('hermes.app').run(['$rootScope', function (rootScope) {
        rootScope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
            console.log('stateChangeSuccess');
            console.log(toState);
            console.log(toParams);
            console.log(fromState);
            console.log(fromParams);
        });
    }]);

})();