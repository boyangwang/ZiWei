var config = require("./config/config.js");

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
app.use(express.cookieParser(config.secret));
app.use(express.session({secret: config.secret}));
app.use(express.logger('dev'));
app.use(express.bodyParser());
app.use(express.methodOverride());
app.use(app.router);
app.use(express.static(__dirname + '/public'));
app.use(express.favicon(__dirname + '/public/img/favicon.ico'));
app.listen(config.port);
console.log("Express is listening on port: " + config.port
            + " in " + config.env + " mode");