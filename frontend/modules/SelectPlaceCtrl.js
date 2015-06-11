(function (angular) {
    'use strict';

    angular.module('tw').controller('SelectPlaceCtrl', function($scope) {
        $scope.cities = Object.keys(tw.data.locations);     
        $scope.getDistrictsOfCity = function(city) {
            var cityObject = tw.data.locations[city];
            $scope.districts = Object.keys(cityObject);
        }
    });
    
})(angular);