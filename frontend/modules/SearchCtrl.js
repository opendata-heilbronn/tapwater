(function (angular) {
  'use strict';
  angular.module('tw').controller('SearchCtrl', function($scope){
        $scope.city = Object.keys(tw.data.locations);      
  }  
  );
})