var geolocate = {
    googleApiKey: "",
    hereMapsAppCode: "",
    hereMapsAppId: "",
    useGoogleApi: true,
    noSupportError: "",
    timeoutError: "",
    unknownError: "",
    positionError: "",
    geolocationApiError: "",
    noDataPreError: "",
    noDataAfterError: ""
};

/**
 * Init info textbox
 */
var info = document.getElementById("info");

/**
 * Define options for getCurrentPosition
 */
var optionsGeoLocating = {
    enableHighAccuracy: true,
    timeout: 7000,
    maximumAge: 0
};

/**
 * Start the reverse geocoding
 * @param pos(position)
 */
var geoLocationSuccessful = function(pos) {
    var crd = pos.coords;
    getReverseGeocodingData(crd);
    tw.locate = "True";
    $.LoadingOverlay("hide");
};

/**
 * Get the error when it is not possible to get the current position by HTML5 browser API
 * If Chrome > v50 (and https is neccessary) use the Google Geocoding API instead of the browser API
 * @param err(Error)
 */
var geoLocationError = function(err) {
    $.LoadingOverlay("hide");
    switch (err.code) {
        case err.TIMEOUT:
            info.innerHTML = geolocate.timeoutError;
            break;
        case err.PERMISSION_DENIED:
            if(err.message.indexOf("Only secure origins are allowed") == 0) {
                tryAPIGeolocation();
            }
            break;
        case err.POSITION_UNAVAILABLE:
            info.innerHTML = geolocate.positionError;
            break;
        case error.UNKNOWN_ERROR:
            info.innerHTML = geolocate.unknownError;
            break;
    }
};

/**
 * Get the current location
 */
var getLocation = function() {
    $.LoadingOverlay("show");
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(geoLocationSuccessful, geoLocationError, optionsGeoLocating);
    } else {
        info.innerHTML = geolocate.noSupportError;
    }
};

/**
 * Get the current location by using the Google Geolocate API
 * IMPORTANT: Insert your own Google Geolocate API Key in the config file.
 */
var tryAPIGeolocation = function() {
    jQuery.post( "https://www.googleapis.com/geolocation/v1/geolocate?key=" + geolocate.googleApiKey, function(success) {
        apiGeolocationSuccess({latitude: success.location.lat, longitude: success.location.lng});

    })
        .fail(function(err) {
            info.innerHTML = geolocate.geolocationApiError + err;
        });
};

/**
 * Start getReverseGeocodingData
 */
var apiGeolocationSuccess = function(position) {
    getReverseGeocodingData(position);
};

/**
 * Get the nearest place (with city, district, street) by coordinate and Here Maps REST API
 * IMPORTANT: Insert your own app_id and app_code in the config file.
 * @param lat(latitude)
 * @param lng(longitude)
 */
var getCurrentPlaceByHere = function(lat, lng){
    return $.getJSON('https://reverse.geocoder.cit.api.here.com/6.2/reversegeocode.json?app_id=' + geolocate.hereMapsAppId + '&app_code=' + geolocate.hereMapsAppCode + '&gen=9&mode=trackPosition&pos=' + lat + ',' + lng).then(function(data){
        return {
            city:data.Response.View["0"].Result["0"].Location.Address.City,
            district:data.Response.View["0"].Result["0"].Location.Address.District,
            street:data.Response.View["0"].Result["0"].Location.Address.Street
        }
    });
};

/**
 * Get the nearest place (with city, district, street) by coordinate and Google Maps Geocoding API
 * IMPORTANT: Insert your own Google Maps Geocoding API Key in the config file.
 * @param lat(latitude)
 * @param lng(longitude)
 */
var getCurrentPlaceByGoogle = function(lat, lng){
    return $.getJSON('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + lat + ',' + lng + '&sensor=true&key=' + geolocate.googleApiKey).then(function(data){
        for (var i=0; i<data.results[0].address_components.length; i++) {
            if (data.results[0].address_components[i].types[0] == "locality") {
                city = data.results[0].address_components[i].long_name;
            }
            if ((data.results[0].address_components[i].types).indexOf("sublocality") > -1) {
                district = data.results[0].address_components[i].long_name;
            }
            if (data.results[0].address_components[i].types[0] == "route") {
                street = data.results[0].address_components[i].long_name;
            }
        }
        if (typeof district == 'undefined') {
            region="";
        }
        return {
            city:city,
            district:district,
            street:street
        }
    });
};

/**
 * Get the nearest place (with city, district, street) by coordinate.
 * @param position
 */
var getReverseGeocodingData = function(position) {
    var lat = position.latitude;
    var lng = position.longitude;

    // Using Here Maps REST API or Google Maps Geocoding API
    if (geolocate.useGoogleApi == "False"){
        getCurrentPlaceByHere(lat, lng).then(function(returndata) {
            //received data!
            var exists = 0 != returndata.city.length;
            if (exists == true){
                $("#city").val(returndata.city).change();
                tw.position = returndata;
                $("#search").click();
            }
            else {
                info.innerHTML = geolocate.noDataPreError + returndata.city + geolocate.noDataAfterError;
            }
        });
    }
    else {
        getCurrentPlaceByGoogle(lat, lng).then(function(returndata) {
            //received data!
            var exists = 0 != returndata.city.length;
            if (exists == true){
                $("#city").val(returndata.city).change();
                tw.position = returndata;
                $("#search").click();
            }
            else {
                info.innerHTML = geolocate.noDataPreError + returndata.city + geolocate.noDataAfterError;
            }
        });
    }
};
