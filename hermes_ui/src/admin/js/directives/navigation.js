(function () {

    var dependencies, navigation;

    navigation = function ($state) {
        var tabs = [], states;

        states = $state.get();

        states.forEach(function (state) {
            if (state.data && state.data.tab) {
                tabs.push({
                    state: _.first(state.name.split('.')),
                    label: state.data.label,
                    url: $state.href(state.name)
                });
            }
        });

        return {
            scope: {},
            templateUrl: 'templates/directives/navigation.html',
            link: function(scope) {
                scope.tabs = tabs;
                scope.isActive = function(tab) {
                    return $state.includes(tab.state);
                };
            }
        };
    };

    dependencies = [
        '$state',
        navigation
    ];

    angular.module('hermes.directives').directive('hermesNavigation', dependencies);

})();