(function (angular) {
    'use strict';

    angular.module('tw').controller('SelectPlaceCtrl', function($scope, $http) {
        $scope.cities = Object.keys(tw.data.locations);     
        $scope.getDistrictsOfCity = function(city) {
            var cityObject = tw.data.locations[city];
            $scope.districts = Object.keys(cityObject);
        }
        $scope.$on('location', function(event, latLon) {
            $http.get('http://localhost:8012/geocode?lat=' + latLon.lat + '&lon' + latLon.lon).success(function(data) {
                console.log(data);
            })
        })
    });
    
})(angular);