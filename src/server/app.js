var config = require("./config/config.js");
var favicon = require('serve-favicon');
var mongodb = require('mongodb');
mongodb.Db.connect('mongodb://localhost:27017/ziwei', function(err, db) {
	console.log('connecting to mongodb');
	if (err) {
		console.log(err);
	}
	else {
		GLOBAL.Db = db;
    }
});

var express = require("express");
var app = express();
app.use(express.static(__dirname + '/public'));
app.use(favicon(__dirname + '/public/img/favicon.ico'));
app.listen(config.port);
console.log("Express is listening on port: " + config.port
            + " in " + config.env + " mode");