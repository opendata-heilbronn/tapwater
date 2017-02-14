var process = require('process');
var mongoSetup = require('./mongo-setup');
var heilbronnPlaces = require('./hn-streets.json');
var zones = require('./zones.json');

var GeoJSON = require('mongoose-geojson-schema');
var mongoose = require('mongoose');

    mongoose.connect('mongodb://localhost/tapwater');

    var Location = mongoose.model('Location', new mongoose.Schema({
        name: String,
        zone: String,
        geometry: GeoJSON.Geometry
    }));
    var Zone = mongoose.model('Zone', {
        name: String,
        calcium: Number,
        kalium: Number
    });


var convertCoordinatesArray = function (coordinates) {
    var convertedCoordinates = [];
    coordinates.forEach(function (coordinate) {
        if (Array.isArray(coordinate[0])) {
            convertedCoordinates.push(convertCoordinatesArray(coordinate));
        } else {
            convertedCoordinates.push([coordinate[1], coordinate[0]]);
        }
    });
    return convertedCoordinates;
};

heilbronnPlaces.features.forEach(function (feature) {
    var location = new Location({
        name: feature.properties.name,
        zone: "Heilbronn " + feature.properties.haertegrad,
        geometry: {
            "type": feature.geometry.type,
            "coordinates": convertCoordinatesArray(feature.geometry.coordinates)
        }
    });
    location.save(function(e) {
        console.log(e);
    });
});

Object.keys(zones).forEach(function (zoneName) {
    var zone = new Zone({
        name: zoneName,
        calcium: zones[zoneName].calcium,
        kalium: zones[zoneName].kalium
    });
    zone.save();
});

process.exit();