(function () {

    var dependencies, fileDirective;

    /**
     * this directive should handle progressbar
     * display message of file stuff
     *
     * @returns {{scope: {clearFile: string}, restrict: string, link: Function}}
     */
    fileDirective = function () {
        return {
            scope: {
                clearFile: '='
            },
            restrict: 'A',
            link: function (scope, element, attr) {
                scope.$watch('clearFile', function (value) {
                    if (value === true) {
                        scope.clearFile = false;
                        element.val('');
                    }
                });
            }
        };
    };

    dependencies = [
        fileDirective
    ];

    angular.module('hermes.directives').directive('hermesFileField', dependencies);

})();