(function (angular) {
    'use strict';
    var heightOfBar = 400;
    angular.module('tw').controller('PlaceCtrl', function($scope, $routeParams) {
        $scope.placeID = $routeParams.id;
        $scope.minerals = Object.keys(tw.data.minerals);
        $scope.getPlaceValue = function(mineralName) {
            var zoneObject = tw.data.zones[$routeParams.id];
            return zoneObject[mineralName];      
        }
        $scope.getMineralMax = function(mineralName) {
            return tw.data.minerals[mineralName][0];
        }
        $scope.getMineralLegalLimit = function(mineralName) {
            return tw.data.minerals[mineralName][1];
        }
        $scope.calculateHeight = function(mineralName) {
            var calculatedHeight = heightOfBar / $scope.getMineralMax(mineralName) * $scope.getPlaceValue(mineralName);
            return calculatedHeight;
        }
        
    });
})(angular);