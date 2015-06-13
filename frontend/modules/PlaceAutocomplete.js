(function (angular) {
	angular.module('tw').directive('placeAutocomplete', function () {
		return {
			restrict: 'A',
			link: function (scope, element) {
				var autocomplete = new google.maps.places.Autocomplete(
				element[0],	{ types: ['geocode'] });
				google.maps.event.addListener(autocomplete, 'place_changed', function () {
					 var place = autocomplete.getPlace();
					 console.log(place);
				});
			}
		};
	});
})(angular);
