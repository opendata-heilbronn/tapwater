(function (angular) {
    'use strict';

    angular.module('tw').controller('SelectPlaceCtrl', function($scope) {
        $scope.cities = Object.keys(tw.data.locations);
    });
})(angular);