(function () {
    var dependencies;

    angular.module('hermes.controllers', []);
    angular.module('hermes.services', []);
    angular.module('hermes.directives', []);
    angular.module('hermes.filters', []);

    angular.module('hermes.core', ['hermes.controllers', 'hermes.services', 'hermes.directives', 'hermes.filters']);
    dependencies = [
        'hermes.core',
        'hermes.templates',
        'ui.router',
        'ui.bootstrap',
        'ngFileUpload'
    ];

    angular.module('hermes.app', dependencies);
})();