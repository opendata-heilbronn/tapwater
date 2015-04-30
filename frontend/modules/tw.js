var tw = {
    data: {}
};
(function (angular) {
    'use strict';
    angular.module('tw', ['ngRoute', 'ngMaterial']);
    angular.module('tw').run(function ($rootScope) {
        $rootScope.page = {title: ''};
    });
    angular.module('tw').config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                controller: 'SelectPlaceCtrl',
                templateUrl: 'modules/partials/selectPlace.html'
            })
            .when('/place/:id', {
                controller: 'PlaceCtrl',
                templateUrl: 'modules/partials/place.html'
            });
    });
})(angular);