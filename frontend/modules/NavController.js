(function (angular) {
    'use strict';
    angular.module('tw').controller('NavController', function($scope, $location) {
       $scope.goto = function() {
           $location.path("/contact")
       }
       $scope.goti = function() {
           $location.path("/about")
       }
       $scope.gota = function() {
           $location.path("/participants")           
       }
       $scope.gotu = function() {
           $location.path("/impressum")           
       }
    });
})(angular);