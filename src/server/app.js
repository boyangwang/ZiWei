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
app.use(require('body-parser').urlencoded({ extended: true }));
app.use(express.static(__dirname + '/public'));
app.use(favicon(__dirname + '/public/img/favicon.ico'));
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');
app.listen(config.port);

var handlePostZiWeiPan = function(app, req, res) {
	// 1. based on req.body, create name string
	// retrieve pan object, or it doesn't exist
	var inputs = req.body;
	var name = ['y', (inputs['y']).toString(), 'm', (inputs['m']).toString(), 'd', (inputs['d']).toString(), 'h', (inputs['h']).toString(), 'sex', (inputs['sex']).toString(), 'mode', (inputs['mode']).toString()].join('-') + '.json';
	var panObj = null;
	console.log('name: ', name);
	GLOBAL.Db.collection('zhycw', function(err, collection) {
        collection.findOne({'name': name}, function(err, item) {
        	resultPage = 'default';
            if (item == null) {
        		res.render('notFound');
            }
            else {
            	console.log(item)
            	res.render('ZiWeiPan', item);
            }
        });
    });
}

app.post('/ZiWeiPan', handlePostZiWeiPan.bind(null, app));

console.log("Express is listening on port: " + config.port
            + " in " + config.env + " mode");