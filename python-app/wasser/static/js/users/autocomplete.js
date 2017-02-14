//arguments to narrow the google maps results
var options = {
    types: ['(regions)'],
    componentRestrictions: {country: "de"}
};
//autocomplete function
google.maps.event.addDomListener(window, 'load', intilizeAutocomplete);
function intilizeAutocomplete() {
    var autocomplete = new google.maps.places.Autocomplete(document.getElementById('city'), options);

    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        // get the values from autocomplete result
        var place = autocomplete.getPlace();
        var location = place.formatted_address;
        //split address string to get name of city and country
        var address= location.split(/,/);
        var city = address[0];
        //var country = address[1];
        //var lat = place.geometry.location.lat();
        //var lng = place.geometry.location.lng();
        city = city.replace(/[0-9]/g, '');
        city = $.trim(city);

        //return the variable city back to input field city
        document.getElementById('city').value = city;
    });
}
