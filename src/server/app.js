
var config = require("./config/config.js");
var favicon = require('serve-favicon');
var mongodb = require('mongodb');
mongodb.MongoClient.connect('mongodb://localhost:27017/ziwei', function(err, db) {
	console.log('connecting to mongodb');
	if (err) {
		console.log(err);
	}
	else {
		GLOBAL.Db = db;
    }
});
var fs = require('fs');
var express = require("express");
var app = express();
app.use(require('body-parser').urlencoded({ extended: true, limit: '50mb' }));
app.use(express.static(__dirname + '/public'));
app.use(favicon(__dirname + '/public/img/favicon.ico'));
app.set('view engine', 'ejs');
app.set('views', __dirname + '/views');
app.listen(config.port);

var starList = ['', "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府", "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军", "文昌", "文曲", "左辅", "右弼", "天魁", "天钺", "擎羊", "陀罗", "火星", "铃星", "地空", "地劫", "禄存", "天马", "天官", "天福", "天厨", "天刑", "天姚", "解神", "天巫", "天月", "阴煞", "台辅", "封诰", "天空", "天哭", "天虚", "龙池", "凤阁", "红鸾", "天喜", "孤辰", "寡宿", "蜚廉", "破碎", "51", "52", "天德", "月德", "天才", "天寿", "三台", "八座", "恩光", "天贵", "截空", "旬空", "天使", "天伤", "博士", "力士", "青龙", "小耗", "将军", "奏书", "飞廉", "喜神", "病符", "大耗", "伏兵", "官府", "将星", "攀鞍", "岁驿", "息神", "华盖", "劫煞", "灾煞", "天煞", "指背", "咸池", "月煞", "亡神", "岁建", "晦气", "丧门", "贯索", "官符", "小耗", "大耗", "龙德", "白虎", "天德", "吊客", "病符"];
GLOBAL.starExplanation = require('./starExplanation.json');

var handlePostZiWeiPan = function(app, req, res) {
	// 1. based on req.body, create name string
	// retrieve pan object, or it doesn't exist
	var inputs = req.body;
    console.log(inputs);
    searchPanRenderPage(inputs, res, inputs);	
}

var searchPanRenderPage = function(inputs, res, origInputs) {
    // generated name string from currentInputs
    var name = getNameFromInputs(inputs);
    console.log('name: ', name);
    GLOBAL.Db.collection('zhycw', function(err, collection) {
        collection.findOne({'name': name}, function(err, item) {

            if (item == null) { // not found
                previousInputs = forgePreviousInputs(inputs);
                // if (isIdentical(nextInputs, origInputs)) {
                //     res.render('notFound');
                // }
                searchPanRenderPage(previousInputs, res, origInputs);
            }
            else { // found
                foundItemAndRender(item, origInputs, res);
            }
        });
    });
}

var forgePreviousInputs = function(inputs) {
    var prev = {};
    prev = completeCopy(inputs);
    if (prev.h != 0) {
        prev.h = prev.h - 2;
        return prev;
    }
    prev.h = 22;
    if (prev.d != 1) {
        prev.d = prev.d - 1;
        return prev;
    }
    prev.d = 28;
    if (prev.m != 1) {
        prev.m = prev.m - 1;
        return prev;
    }
    prev.m = 12;
    prev.y = prev.y - 1;
    return prev;
}

var completeCopy = function(inputs) {
    var obj = {};
    obj.y = inputs.y;
    obj.m = inputs.m;
    obj.d = inputs.d;
    obj.h = inputs.h;

    obj.sex = inputs.sex;
    obj.mode = inputs.mode;
    return obj;
}

var isIdentical = function(inputsA, inputsB) {

}

var foundItemAndRender = function(item, origInputs, res) {
    item.starList = starList;           
    item.starExplanation = GLOBAL.starExplanation;
    item.data.inputs.name = origInputs.name;

    item = replaceWithOrigInputs(item, origInputs);

    console.log(item);
    res.render('ZiWeiPan', item);
}


var getNameFromInputs = function(inputs) {
    var name = ['y', (inputs['y']).toString(), 'm', (inputs['m']).toString(), 'd', (inputs['d']).toString(), 'h', (inputs['h']).toString(), 'sex', (inputs['sex']).toString(), 'mode', (inputs['mode']).toString()].join('-') + '.json';
    return name;
}

var replaceWithOrigInputs = function(item, origInputs) {
    // 公历:1930年01月01日0时生
    // 农历:己巳年12月02日子时生
    /*    <option value="0" id="ljms_OPTION_20">
            子时 23:00-0:59
          </option>
          <option value=2 id="ljms_OPTION_22">
            丑时 1:00-2:59
          </option>
          <option value=4 id="ljms_OPTION_24">
            寅时 3:00-4:59
          </option>
          <option value=6 id="ljms_OPTION_26">
            卯时 5:00-6:59
          </option>
          <option value=8 id="ljms_OPTION_28">
            辰时 7:00-8:59
          </option>
          <option value=10 id="ljms_OPTION_30">
            巳时 9:00-10:59
          </option>
          <option value=12 id="ljms_OPTION_32">
            午时 11:00-12:59
          </option>
          <option value=14 id="ljms_OPTION_34">
            未时 13:00-14:59
          </option>
          <option value=16 id="ljms_OPTION_36">
            申时 15:00-16:59
          </option>
          <option value=18 id="ljms_OPTION_38">
            酉时 17:00-18:59
          </option>
          <option value=20 id="ljms_OPTION_40">
            戌时 19:00-20:59
          </option>
          <option value=22 id="ljms_OPTION_42">
            亥时 21:00-22:59
          </option>
    */

    var solar = item['data']['centerGong']['阳历生日'];
    var lunar = item['data']['centerGong']['阴历生日'];

    solar = changeYear(solar, origInputs);
    solar = changeMonth(solar, origInputs);
    solar = changeDay(solar, origInputs);
    solar = changeHour(solar, origInputs);
    item['data']['centerGong']['阳历生日'] = solar;

    // lunar = changeMonth(lunar, origInputs);
    // lunar = changeDay(lunar, origInputs);
    lunar = changeLunarHour(lunar, origInputs);
    //TODO lunar hour
    item['data']['centerGong']['阴历生日'] = lunar;
    return item;
}

var changeLunarHour = function(old, inputs) {
    var map = {
        0: '', 2: '子',4: '丑',6: '寅',8: '卯',10: '辰',12: '巳',14: '午',16: '未',18: '申',20: '酉',22: '戌', 24: '亥'
    }
    for (var i=0; i<=22; i+=2) {
        var incremented = i + 2;
        map[i] = map[incremented];
    }
    var lunarHourString = map[inputs.h];
    var idx = old.indexOf('时');
    var idx2 = old.indexOf('日');

    var newString = old.substring(0, idx2+1) + lunarHourString + old.substring(idx);
    return newString;
}

var changeYear = function(old, inputs) {
    var idx = old.indexOf('年');
    var str = '' + inputs.y;
    var newString = str + old.substring(4);

    return newString;
}

var changeMonth = function(old, inputs) {
    var idx = old.indexOf('月');
    var idx2 = old.indexOf('年');
    var str = '' + inputs.m;
    if (str.length == 1) {
        str = '0' + str;
    }
    var newString = old.substring(0, idx2+1) + str + old.substring(idx);
    return newString;
}

var changeDay = function(old, inputs) {
    var idx = old.indexOf('日');
    var idx2 = old.indexOf('月');

    var str = '' + inputs.d;
    if (str.length == 1) {
        str = '0' + str;
    }
    var newString = old.substring(0, idx2+1) + str + old.substring(idx);
    return newString;
}

var changeHour = function(old, inputs) {
    var idx = old.indexOf('时');
    var str = '' + inputs.h;
    if (str.length == 1) {
        str = '0' + str;
    }
    var former = old.substring(0, old.indexOf('日') + 1);
    var latter = old.substring(idx);;
    old = former + str + latter
    return old;
}

var replaceWithOrigD = function(item, origD) {
    
    var origDString = origD >= 10 ? origD.toString() : '0' + origD.toString();
    
    item['data']['centerGong']['阳历生日'][9] = origDString[0];
    item['data']['centerGong']['阳历生日'][10] = origDString[1];
    return item;
}

app.post('/ZiWeiPan', handlePostZiWeiPan.bind(null, app));
app.get('/ZiWeiPan', function(req, res) { res.redirect('/'); });
app.get('/jiexi', function(req, res) { res.render('jiexi'); });
app.post('/jiexi', function(req, res) {
    console.log(req.body);
    if (req && req.body && req.body.password == 'password') {
        res.status(200).json(GLOBAL.starExplanation);
    }
    else {
        res.status(401).json({});
    }
});
app.put('/jiexi', function(req, res) {
    console.log(req.body);
    fs.writeFileSync('./starExplanation.json', JSON.stringify(req.body)); 
    // console.log(require.cache.keys());
    // fs.writeFileSync('./require.cache.json', JSON.stringify(require.cache, null, 2)); 
    delete require.cache[require.resolve('./starExplanation.json')];
    GLOBAL.starExplanation = require('./starExplanation.json');
    res.status(200).json({});
});


console.log("Express is listening on port: " + config.port
            + " in " + config.env + " mode");