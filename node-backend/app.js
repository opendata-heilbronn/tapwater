var GeoJSON = require('mongoose-geojson-schema');
var mongoose = require('mongoose');
var process = require('process');
mongoose.connect('mongodb://localhost/tapwater');

var Location = mongoose.model('Location', new mongoose.Schema({geoFeature: GeoJSON.Feature}));
var Zone = mongoose.model('Zone', {
    name: String,
    calcium: Number,
    kalium: Number
});

var sampleZone = new Zone({
    name: 'Erlenbach',
    calcium: 0.8,
    kalium: 0.9
});
sampleZone.save();

console.log('done');
process.exit();