(function (angular) {
    angular.module('tw').directive('locateMeButton', function () {
        return {
            restrict: 'A',
            link: function (scope, elem) {
                elem.on('click', function () {
                    scope.$emit('location', {lat: 1, lon: 2});
                });
            }
        }
    });
})(angular);