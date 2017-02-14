var GeoJSON = require('mongoose-geojson-schema');
var mongoose = require('mongoose');
var express = require('express');
var baucis = require('baucis');
var cors = require('cors');
var mongoSetup = require('./mongo-setup');
var mongo = mongoSetup.setupInstance();

// rest
baucis.rest('Zone');

// start http server
var app = express();
app.use(cors());
app.use('/api', baucis());
app.listen(8012);

app.get('/geocode', function (req, res) {
    res.send("Latitude " + req.query.lat + ", Longitude " + req.query.lon + ' has the following mineral values in its tapwater: calcium 0.8, natrium 2, nitrat 5 - you have a good tapwater!');
});