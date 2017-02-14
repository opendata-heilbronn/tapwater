(function (angular) {
    angular.module('tw').directive('geocodeAddress', function () {
        return {
            restrict: 'A',
            link: function (scope, elem) {
                var autocomplete = new google.maps.places.Autocomplete(elem[0]);
                google.maps.event.addListener(autocomplete, 'place_changed', function () {
                    console.log(autocomplete.getPlace());
                });
            }
        }
    });
})(angular);