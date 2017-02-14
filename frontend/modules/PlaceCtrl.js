(function (angular) {
    'use strict';
    var heightOfBar = 420;
    var heightOfMaxScale = 400;
    angular.module('tw').controller('PlaceCtrl', function($scope, $routeParams) {
        $scope.placeID = $routeParams.id;
        $scope.minerals = Object.keys(tw.data.minerals);
        $scope.getPlaceValue = function(mineralName) {
            var zoneObject = tw.data.zones[$routeParams.id];
            return zoneObject[mineralName];      
        }
        
        $scope.scanMineralMax = function(mineralName) {
            var mineralMax = 0;
            var mineralValue = 0;
            Object.keys(tw.data.zones).forEach(function(key) {
                mineralValue = tw.data.zones[key][mineralName]
                if (!isNaN(mineralValue) && mineralValue > mineralMax){
                    mineralMax = mineralValue; 
                }
            }      
            )
            return mineralMax;
        }   
        
        $scope.mineralAverage = function(mineralName) {
            var mineralValue = 0;
            var mineralSum = 0;
            var mineralAverage = 0;
            var i = 0;
            Object.keys(tw.data.zones).forEach(function(key) {
                mineralValue = tw.data.zones[key][mineralName];
                if (!isNaN(mineralValue) && mineralValue) {
                    mineralSum = mineralSum + parseInt(mineralValue,10);
                    i++;
                }
            }
            )
            console.log (mineralSum, i);
            mineralAverage = mineralSum / i;    
            return mineralAverage;
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
        $scope.calculateScaleValues = function(mineralName) {
            var scaleHeight = heightOfMaxScale;
            var scaleValueArray=[];
            for (var i = 0; i <= 4; i++) {
                scaleValueArray[i] = $scope.getMineralMax(mineralName) / heightOfMaxScale * scaleHeight;
                scaleHeight = scaleHeight-100;
            }
            return scaleValueArray;            
        }
        
    });
})(angular);