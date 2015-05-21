(function (angular) {
    'use strict';
    angular.module('tw').controller('PlaceCtrl', function($scope, $routeParams) {
        $scope.placeID = $routeParams.id;
        $scope.placevalues = tw.data.zones[$routeParams.id];
        $scope.calculateHeight = function(key, value) {
            console.log (tw.data.mineralMax)
            var mineralMax = tw.data.mineralMax[key];
            var calculatedHeight = 400 / mineralMax * value;
            return calculatedHeight;
        }
    });
})(angular);