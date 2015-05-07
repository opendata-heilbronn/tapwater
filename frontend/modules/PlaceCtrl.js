(function (angular) {
    'use strict';
    angular.module('tw').controller('PlaceCtrl', function($scope, $routeParams) {
        $scope.placeID = $routeParams.id;
        $scope.placevalues = tw.data.zones[$routeParams.id];
    });
})(angular);