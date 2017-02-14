var GeoJSON = require('mongoose-geojson-schema');
var mongoose = require('mongoose');

exports.setupInstance = function() {
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

    return {
        location: Location,
        zone: Zone
    };
};
