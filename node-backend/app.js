var GeoJSON = require('mongoose-geojson-schema');
var mongoose = require('mongoose');
var express = require('express');
var baucis = require('baucis');
var cors = require('cors');
mongoose.connect('mongodb://localhost/tapwater');

// define models
var Location = mongoose.model('Location', new mongoose.Schema({geoFeature: GeoJSON.Feature}));
var sampleLocation = new Location({
    geoFeature: {
        "type": "Feature",
        "properties": {
            "haertegrad": "10",
            "name": "Aachener Straße"
        },
        "geometry": {
            "type": "MultiLineString",
            "coordinates": [[[9.1054195, 49.1836073], [9.1053332, 49.1833407], [9.1051728, 49.1828456], [9.1051326, 49.1828453], [9.1046133, 49.1828413]], [[9.1051326, 49.1828453], [9.1049988, 49.1830276], [9.1048492, 49.1832862]], [[9.1051728, 49.1828456], [9.1053677, 49.1827792], [9.1066049, 49.1825795]]]
        }
    }
});
sampleLocation.save();


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

// rest
baucis.rest('Zone');

// start http server
var app = express();
app.use(cors());
app.use('/api', baucis());
app.listen(8012);

app.get('/geocode', function(req, res) {
    res.send("Latitude " + req.query.lat + ", Longitude " + req.query.lon + ' has the following mineral values in its tapwater: calcium 0.8, natrium 2, nitrat 5 - you have a good tapwater!');
});