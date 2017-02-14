(function (angular) {
	angular.module('tw').directive('locateMeButton', function () {
		return {
			restrict: 'A',
			link: function (scope, element) {
				element.on('click', function () {
					if (navigator.geolocation) {
						navigator.geolocation.getCurrentPosition(showPosition);
					} else {
						alert("Geolocation is not supported by this browser.");
					}
					function showPosition(position) {
						console.log(position);	
					}
				});
			}
		};
	});
})(angular);
