(function (angular) {
    'use strict';

    angular.module('tw').controller('SelectPlaceCtrl', function($scope) {
        $scope.cities = Object.keys(tw.data.locations);     
        $scope.getDistrictsOfCity = function(city) {
            $scope.districts = Object.keys(tw.data.locations[city]);
        }
    });
    
})(angular);