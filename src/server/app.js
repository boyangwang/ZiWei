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

var starList = ['', "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军", "文昌", "文曲", "左辅", "右弼", "天魁", "天钺", "擎羊", "陀罗", "火星", "铃星", "地空", "地劫", "禄存", "天马", "天官", "天福", "天厨", "天刑", "天姚", "解神", "天巫", "天月", "阴煞", "台辅", "封诰", "天空", "天哭", "天虚", "龙池", "凤阁", "红鸾", "天喜", "孤辰", "寡宿", "蜚廉", "破碎", "51", "52", "天德", "月德", "天才", "天寿", "三台", "八座", "恩光", "天贵", "截空", "旬空", "天使", "天伤", "博士", "力士", "青龙", "小耗", "将军", "奏书", "飞廉", "喜神", "病符", "大耗", "伏兵", "官府", "将星", "攀鞍", "岁驿", "息神", "华盖", "劫煞", "灾煞", "天煞", "指背", "咸池", "月煞", "亡神", "岁建", "晦气", "丧门", "贯索", "官符", "小耗", "大耗", "龙德", "白虎", "天德", "吊客", "病符"];
var starExplanation = require('./starExplanation.js');

var handlePostZiWeiPan = function(app, req, res) {
	// 1. based on req.body, create name string
	// retrieve pan object, or it doesn't exist
	var inputs = req.body;
    console.log(inputs);
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
    			item.starList = starList;        	
    			item.starExplanation = starExplanation;
            	item.data.inputs.name = req.body.name;
            	console.log(item);
            	res.render('ZiWeiPan', item);
            }
        });
    });
}

app.post('/ZiWeiPan', handlePostZiWeiPan.bind(null, app));
app.get('/ZiWeiPan', function(req, res) { res.redirect('/'); });
app.get('/jiexi', function(req, res) { res.render('jiexi'); });
app.post('/jiexi', function(req, res) { 
    console.log(req.body);
    if (req && req.body && req.body.password == 'password') {
        res.status(200).json(starExplanation);
    }
    else {
        res.status(401).json({});
    }
});

console.log("Express is listening on port: " + config.port
            + " in " + config.env + " mode");