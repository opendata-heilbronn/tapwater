(function (angular) {
    'use strict';
    angular.module('tw', ['ngRoute']);
    angular.module('tw').config(function ($locationProvider, $httpProvider) {
        $locationProvider.html5Mode(true);
    });
    angular.module('tw').run(function ($rootScope) {
        $rootScope.page = {title: ''};
    });
})(angular);