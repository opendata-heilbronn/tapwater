'use strict';

var tw = {
	data: {},
    zoneData: {},
    zoneId: "",
    position: {},
    locate: ""
};

var attribute = null, hasSelectedFirstLocation = false, section = 'explanation';
var attributes = ["sodium", "potassium", "calcium", "magnesium", "chloride", "nitrate", "sulfate"];

/**
 * generate the zone id with the given params
 * @param city
 * @param district
 * @param streetZone
 * @returns {string}
 */
var generateZoneId = function(city, district, streetZone) {
    var idParts = [];
    var addIdPart = function(value) {
        if (value && idParts.indexOf(value) < 0) {
            idParts.push(value);
        }
    };

    addIdPart(city);
    addIdPart(district);
    addIdPart(streetZone);
    return idParts.join(' ');
};

/**
 * Update zone info with description and year
 */
var updateZoneInfo = function() {
    if (tw.zoneData) {
        $('.zone-id').text(tw.zoneId.replace("|", ""));
        $('.zone-data-year').text(tw.zoneData.date);
        $('.zone-description').html(tw.zoneData.remarks);
        $('.zone-about').toggle((tw.zoneData.date || tw.zoneData.remarks) ? true : false);
        $('.zone-year-container').toggle(tw.zoneData.date ? true : false);
    }
};

/**
 * Disable Tab, if attribute is not available on zoneData
 */
var updateDisabledTabs = function() {
    $('.nav-li-main').removeClass('disabled');
    attributes.forEach(function(attribute) {
        if (!tw.zoneData[attribute]) {
            $('a[data-toggle="tab"][data-attribute="' + attribute + '"]').parent().addClass('disabled');
        }
    });
};

/**
 * Update info container and gauge
 */
var updateAttributeContent = function() {
    if (attribute === 'info') {
        $('.result-with-value, .result-without-value').hide();
        $('.info-container').show();
    } else {
        $('.info-container').hide();

        if (tw.zoneData && tw.zoneData[attribute]) {
            $('.result-without-value').hide();
            $('.result-with-value').show();

            tw.gauge.update(attribute);
            if (section === 'explanation') {
                tw.gauge.updateValue(attribute, tw.zoneData[attribute], tw.zoneData);
            }
            if (section === 'compare') {
                tw.comparison.update(attribute, tw.zoneData[attribute]);
            }
        } else {
            $('.result-with-value').hide();
            $('.result-without-value').show();
        }
    }
};

/**
 * Setup all mineral tabs
 * @param startAttribute
 */
var setupTabs = function(startAttribute) {
    $('a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        attribute = $(e.target).data('attribute');
        $('.current-attribute-label').text($(e.target).text());
        section = 'explanation';
        updateSection();
        updateAttributeContent();
    });

    var startAttributeElement = $('a[data-attribute="' + startAttribute + '"]');
    startAttributeElement.parent().addClass('active').closest('.nav-li-main').addClass('active');
    $('.current-attribute-label').text(startAttributeElement.text());
    attribute = startAttribute;
};

/**
 * Generate the options output for input select
 * @param values list of values for the content
 * @param withEmptyOption
 * @returns {string} return the html code with options
 */
var generateOptionsHtml = function(values, withEmptyOption) {
    var html = withEmptyOption ? '<option value="">Bitte auswählen</option>' : '';
    values.forEach(function(value) {
        html += '<option value="' + value + '">' + value + '</option>';
    });
    return html;
};

/**
 * Generate the street zones options output
 * @param values array with values
 * @returns {string} Html content
 */
var generateStreetZonesOptionsHtml = function(values) {
    // Define variables
    var html = '';

    values.forEach(function(value) {
        html += '<option value="' + value.location__zone + '|' +
            value.location__street + '">' + value.location__street + '</option>';
    });

    return html;
};

/**
 * Generate the street zones option-group output
 * @param values array with values
 * @returns {string} Html content
 */
var generateStreetZonesOptionsGroupHtml = function(values) {
    // Define variables
    var activeZone = null;
    var html = '';
    var zone = '';
    var street = '';
    var countZones = 0;

    for(var i = 0; i < values.length; i++){
        zone = values[i].location__zone;
        street = values[i].location__street;

        // If new zone, create option group
        if(activeZone !== zone) {
            // If it's not the first zone, first close the tag before we open a new
            if(countZones !== 0) {
                html += '</optgroup>';
                countZones++;
            }
            // Open new group tag
            html += '<optgroup label="' + zone + '">';
            // Set active zone to current
            activeZone = zone;
        }

        html += '<option value="' + zone + '|' + street + '">' + street + '</option>';

        // close last zone
        if(i+1 === values.length) {
            html += '</optgroup>';
        }
    }
    return html;
};

/**
 * Setup the form on application init
 */
var setupForm = function() {
    bindChangeEvent();
    $('.form-choose-location').on('submit', onSubmit);
};

/**
 * Update section
 */
var updateSection = function() {
    $('.section').hide();
    $('.section-' + section).show();
    if ($('body').scrollTop() > $('.result-with-value').offset().top) {
        $('body').scrollTop($('.result-with-value').offset().top);
    }
};

/**
 * Switch to section on button click
 */
var setupSectionSwitch = function() {
    $('.switch-to-section').on('click', function() {
        section = $(this).data('section');
        updateSection();
        updateAttributeContent();
    });
};

/**
 * Calculate referenced water values
 */
var completeReferenceWaters = function() {
    Object.keys(tw.data.referenceWaters).forEach(function(name) {
        var values = tw.data.referenceWaters[name];
        values.hardness = Math.round(((0.14 * values.calcium) + (0.23 * values.magnesium)) * 10) / 10;
    });
};

/**
 * On change event for selection city
 */
var onChangeCity = function() {
    $.LoadingOverlay("show"); // show loading modal
    unbindChangeEvent(); // unbind all change events
    var city = $('#city').val();
    $.when( $.ajax({
        url: tw.dataUrl,
        data: {
            city: city
        },
        dataType: 'json',
        type: 'get'
    })).done(function( data ) {
        showDistrict(data.districts);
        loadStreetZones(city);
    });
};

/**
 * On change event for selection district
 */
var onChangeDistrict = function() {
    $.LoadingOverlay("show"); // show loading modal
    unbindChangeEvent();
    var city = $('#city').val();
    loadStreetZones(city);
};

/**
 * load districts, used in onChangeCity
 * @param city
 */
var loadStreetZones = function(city) {
    var district = $('#district').val();
    $("#slbDistrict").val(district);
    if (!district) {
        district = '';
    }
    $.when($.ajax({
        url: tw.dataUrl,
        data: {
            city: city,
            district: district
        },
        dataType: 'json',
        type: 'get'
    })).done(function( data ) {
        showStreetZones(data.zones, data.street_zone_limit);
        $.LoadingOverlay("hide");
        bindChangeEvent();
    });
};

/**
 * Show district selection box
 * @param districts
 */
var showDistrict = function(districts) {
    var showDistrict = false;

    if (districts.length > 0) {
        showDistrict = true;
        // if only one item which is emtpy, don't show box
        if(districts.length === 1 && districts[0] === "") {
            showDistrict = false;
        }
    }

    if(showDistrict) {
        $('.district').html(generateOptionsHtml(districts));
        $('.select-district').show();
        if(tw.locate == "True" && districts.indexOf(tw.position.district) > -1){
            $('#district').val(tw.position.district);
        }
    } else {
        $('.select-district').hide();
        $('.district').html('');
    }
};

/**
 * Show streetzones selection box
 * @param zones
 * @param street_zone_limit Limit when groups are disabled
 */
var showStreetZones = function(zones, street_zone_limit) {
    var showZone = false;
    if (zones.length > 0) {
        // if only one object with emtpy data, don't show the select box
        if (zones.length == 1) {
            if (zones[0][1] !== "" || zones[0][0] !== "") {
                showZone = true;
            }
        } else {
            showZone = true;
        }
    }
    if (showZone) {
        if (zones.length >= street_zone_limit) {
            // sort streets, because they are sorted by zone
            zones = zones.sort(function (a, b) {
                return a.location__street.localeCompare(b.location__street);
            });
            // generate output without optiongroups
            $('.streetZone').html(generateStreetZonesOptionsHtml(zones));
        } else {
            $('.streetZone').html(generateStreetZonesOptionsGroupHtml(zones));
        }

        $('.select-street').show();

        /*
        var result = zones.filter(function( obj ) {
            if(obj.location__street == tw.position.street){
                return obj.location__zone;
            }
        });
        var found = false;
        for(var i = 0; i < zones.length; i++) {
            if (zones[i].location__street == tw.position.street) {
                found = true;
                break;
            }
        }

        if(tw.locate == "True" && found == true){
            var streetZo = result[0].location__zone + '|' + tw.position.street;
            $('#streetZone').val(streetZo).change();
        }
        */
    } else {
        $('.select-street').hide();
        $('.streetZone').html('');
    }
};

/**
 * Unbind on change event on selections
 */
var unbindChangeEvent = function() {
    $('#district').off('change');
    $('#streetZone').off('change');
};

/**
 * Bind on Change Events on selections
 */
var bindChangeEvent = function() {
    $('#district').on('change', onChangeDistrict);
};

/**
 * Handle on change event, when leaving city
 */
var initCityFocusOut = function() {
    $( "#city" ).focusout(function() {
        var city = $('#city').val();
        if(city !== "") {
            cityToTitleCase();
            onChangeCity();
        }
    });
};

/**
 * Handle on click for search, dont send when city is empty
 */
var initOnClickSearch = function() {
    $( "#search" ).on( "click", function() {
        var city = $('#city').val();
        if (city!=="") {
            cityToTitleCase();
            onChangeCity();
        }
    });
};

/**
 * First char to upper, rest to lowercase on city
 */
var cityToTitleCase = function () {
    var city = $('#city').val();
    var ret = city.charAt(0).toUpperCase() + city.slice(1);
    $('#city').val(ret);
};

/**
 * Init Autocomplete funciton for cities
 * @param url url for ajax call
 */
var initAutocompleteCities = function(url) {
    $("#city").autocomplete({
        source: function (request, response) {
            var term = $('#city').val();
            $.ajax({
                type: "GET",
                url: url,
                dataType: "json",
                data: {
                    term: term
                },
                error: function (xhr, textStatus, errorThrown) {
                    alert('Error: ' + xhr.responseText);
                },
                success: function (data) {
                    response($.map(data.cities, function (item) {
                        return {
                            label: item.city,
                            value: item.city
                        }
                    }));
                }
            });
        }
    });
};

/**
 * Init form location submit and prevent sending with empty values
 */
var initFormLocationSubmit = function() {
    $('#frmLocation').on('submit', function(e){
        e.preventDefault();
        var city = $('#city').val();
        if (city!=="") {
            this.submit();
        }
    });
};

/**
 * Init the tapwater application
 */
tw.initTapwater = function() {
    completeReferenceWaters();
    setupTabs('sodium');
    setupSectionSwitch();
    tw.gauge.init();
    tw.comparison.init();

    // Update zone information and enable Tabs
    updateZoneInfo();
    updateAttributeContent();
    updateDisabledTabs();
};