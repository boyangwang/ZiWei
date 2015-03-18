window.setCentDom = function(dom, idx) {
	console.log(idx);
	console.log($(dom));
	console.log(window.ejs);
	var starList = ejs.starList;
	var starExplanations = ejs.starExplanation;

	var gong = ejs.data.twelveGongs[idx];
	var allMinorStars = [];
	
	
	allMinorStars = allMinorStars.concat(gong.magentaStars);
	allMinorStars = allMinorStars.concat(gong.brownStars);
	allMinorStars = allMinorStars.map(function(currentValue) {return currentValue[0]});
	// allMinorStars = allMinorStars.concat(gong.cyanStars);
	allMinorStars = allMinorStars.concat(gong.blueStars);
	
	console.log('allMinorStars: ', allMinorStars);

	var expDiv = $('.explanation-div');
	var expTitle = $('.explanation-div h3');
	var sampleMain = $('.sample-main');
	var sampleMinor = $('.sample-minor');

	expDiv.empty();
	expDiv.append(expTitle);
	for (var i=0; i<gong.redStars.length; i++) {
		var s = gong.redStars[i];
		var expP = sampleMain.clone();
		expP.removeClass('sample-main');
		var starNumber = s[0];
		var starName = starList[starNumber];
		console.log(starNumber);
		console.log(starName);
		var expTexts = starExplanations[starName]['explanation'];
		var gongName = gong.gongName;
		if (gongName.indexOf('宫') == -1) {
			gongName += '宫';
		}
		console.log(gongName);
		var expText = expTexts[gongName];
		console.log(expTexts);
		console.log(expText);
		expP.html(expText);
		expDiv.append(expP);
	}
	for (var i=0; i<allMinorStars.length; i++) {
		var s = allMinorStars[i];
		var expP = sampleMinor.clone();
		expP.removeClass('sample-minor');
		var starNumber = s;
		var starName = starList[starNumber];
		console.log(starNumber);
		console.log(starName);

		var expText = starExplanations[starName]['explanation'];
		expP.html(expText);
		expDiv.append(expP);	
	}

    for (var i=0; i<gong.cyanStars.length; i++) {
        
        var expP = sampleMinor.clone();
        expP.removeClass('sample-minor');
        var s = gong.cyanStars[i];

        var starNumber = parseInt(s);
        if (isNaN(starNumber)) {
            var starName = s;    
        }
        else {
            var starName = starList[starNumber];    
        }
        
        console.log(starNumber);
        console.log(starName);

        var expText = starExplanations[starName]['explanation'];
        expP.html(expText);
        expDiv.append(expP);
    }
}

window.goToPan = function(mode) {
	var inputs = ejs.data.inputs;
	inputs.mode = mode;
	console.log(inputs);
	var form = $('.invisible-form');
	var keys = ['y', 'm', 'd', 'h', 'min', 'name', 'sex', 'mode'];
	for (var i=0; i<keys.length; i++) {

		var key = keys[i]
		console.log('key: ', key);
		var input = $("<input>").attr("type", "hidden").attr("name", key).val(inputs[key]);
		form.append(input);
	}
	console.log(form.serializeArray());
	console.log(form);
	form.submit(function() {
		console.log('I\'m submitting!');
	});
	form.submit();
}

tg=new Array("甲","乙","丙","丁","戊","己","庚","辛","壬","癸");dz=new Array("子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥");sx=new Array("鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪");w=new Array("木","火","土","金","水");f=new Array("东","南","中","西","北");sz=new Array("一","二","三","四","五","六","七","八","九","十",
"十一","十二","十三","十四","十五","十六","十七","十八","十九","二十",
"廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十");m0=new Array(
0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,1,
0,1,0,1,2,1,0,0,1,1,0,1,1,1,0,1,0,0,1,0,0,1,1,0,
1,1,0,1,1,0,0,1,0,1,0,1,0,1,1,3,0,1,0,1,0,1,0,1,
0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,
0,4,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,1,0,3632)
m1=new Array(
1,0,1,0,0,4,0,1,1,0,1,1,1,0,1,0,0,1,0,0,1,1,0,1,
1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,3,0,1,0,0,1,0,1,
1,0,1,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,0,1,0,
1,2,1,0,1,1,0,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,
0,1,0,0,1,0,3,1,0,1,1,1,0,1,0,0,1,0,0,1,0,1,1,1,7294)
m2=new Array(
1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,1,2,1,0,0,1,0,1,1,
0,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,0,
1,0,1,3,1,0,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,
1,0,0,1,0,1,0,1,0,1,1,1,0,4,0,1,0,0,1,0,1,1,1,1,
0,1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,4,0,1,0,1,1,0,10955);m3=new Array(
1,1,0,1,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,
0,1,1,0,5,0,1,0,1,0,0,1,0,1,0,1,1,0,1,0,1,1,0,1,
0,0,1,0,1,0,1,1,0,1,1,0,1,0,3,0,0,1,1,0,1,1,1,0,
1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,3,0,1,1,0,1,
1,1,0,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,14587);m4=new Array(
1,1,0,1,1,3,0,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,
0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,3,0,1,0,1,1,0,1,1,
0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,0,1,0,1,1,0,1,
1,4,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,
1,0,1,1,0,1,2,1,0,1,0,1,0,1,1,0,1,1,0,0,1,0,1,0,18249);m5=new Array(
1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,3,0,1,1,0,1,0,1,
0,1,0,0,1,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,
0,1,3,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,
1,0,1,0,1,0,0,4,1,0,1,0,1,1,1,0,1,0,0,1,0,1,0,1,
0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,4,1,0,1,0,1,0,21911);m6=new Array(
1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,
1,0,1,2,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,1,
0,1,0,1,0,0,1,0,0,1,1,0,1,1,4,1,0,0,1,0,0,1,1,0,
1,1,0,1,1,0,0,1,0,1,0,1,0,1,0,1,1,0,4,1,0,1,0,1,
0,1,0,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,1,25544);m7=new Array(
0,1,0,0,4,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,
1,0,1,0,0,1,0,0,1,1,0,1,1,1,0,4,0,1,0,0,1,1,0,1,
1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,1,0,4,0,1,0,1,
1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,1,0,1,0,
1,0,0,1,0,5,0,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,29206);m8=new Array(
0,1,0,0,1,0,0,1,1,0,1,1,1,0,1,2,1,0,0,1,0,1,1,1,
1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,0,4,1,1,
0,1,1,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1,0,1,0,0,
1,0,1,0,1,4,1,1,0,1,0,0,1,0,1,0,1,0,1,1,0,1,1,0,
1,0,0,1,0,1,0,1,0,1,1,1,0,1,0,0,4,0,1,0,1,1,1,1,32868);m9=new Array(
0,1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,0,1,0,1,1,
0,1,4,1,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,
0,1,1,0,1,0,1,4,0,1,0,1,0,1,0,1,1,0,1,0,1,1,0,0,
1,0,1,0,1,0,1,1,0,1,1,0,1,0,0,1,2,1,1,0,1,1,0,1,
1,0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,0,1,0,1,1,0,36499);m10=new Array(
1,1,0,4,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,
1,1,0,1,1,0,1,0,0,1,0,1,0,4,1,1,0,1,0,1,0,1,0,1,
0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,4,1,1,0,1,1,
0,0,1,0,0,1,0,1,1,1,0,1,1,0,0,1,0,0,1,0,1,1,0,1,
1,1,0,0,4,0,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,40161);m11=new Array(
1,0,1,1,0,1,0,0,1,0,1,0,1,0,1,4,1,0,1,0,1,0,1,0,
1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,4,1,0,1,
0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,
0,1,0,1,0,3,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1,0,1,1,
1,0,1,0,1,0,0,1,0,0,1,1,0,1,1,4,1,0,0,1,0,1,0,1,43823);m12=new Array(
0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,
0,4,0,1,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,
1,0,1,0,0,4,1,0,1,1,1,0,1,0,1,0,0,1,0,0,1,1,1,0,
1,1,0,1,0,0,1,0,0,1,1,0,1,1,1,0,4,0,1,0,0,1,1,0,
1,1,0,1,0,1,0,1,0,0,1,1,0,1,0,1,1,0,1,0,1,0,1,0,47455)
m13=new Array(
0,1,4,1,0,1,1,0,1,0,1,0,1,0,0,1,0,1,1,0,1,1,0,1,
0,1,0,0,1,0,1,0,1,1,4,1,0,1,0,0,1,0,1,0,1,1,0,1,
1,0,1,0,0,1,0,0,1,1,0,1,1,1,0,1,0,3,0,0,1,0,1,1,
1,1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1,0,0,
1,1,0,1,4,1,0,1,0,1,0,0,1,0,1,1,0,1,0,1,1,0,1,0,51117)
m14=new Array(
0,1,0,1,0,1,1,0,1,1,0,1,0,4,0,1,0,1,0,1,1,0,1,1,
0,1,0,0,1,0,0,1,1,0,1,1,1,0,1,0,0,1,2,1,0,1,1,1,
1,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,0,1,0,1,
1,0,1,1,3,0,1,0,0,1,0,1,0,1,1,0,1,1,0,1,0,0,1,0,
1,0,1,0,1,1,0,1,1,0,1,0,0,1,3,0,1,0,1,1,0,1,1,0,54779)
ms=new Array(m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14);ly=new Array(29,30,58,59,59,60);tw=new Array(0,0,1,1,2,2,3,3,4,4);dw=new Array(4,2,0,0,2,1,1,2,3,3,2,4);


function inq(form) {
    if (ejs.data['centerGong'].hasOwnProperty('八字')) {
        window.scbz = ejs.data['centerGong']['八字'];
        return;
    }



	console.log(form);
    re = "请重新输入！";
    y = form.y;
    if (y == "" || y < 1901 || y > 2050)
        alert("年应在1901和2050之间。" + re);
    else {
        gl0 = (Date.UTC(y, 0, 1) - Date.UTC(1901, 1, 19)) / 86400000;
        dy = y - 1901;
        i = Math.floor(dy / 10);
        nl0 = (i == 0) ? 0 : ms[i - 1][120];
        n = i * 120;
        for (j = 0; j < 120; j++) {
            n++;
            if (n > dy * 12) break;
            nl0 += ly[ms[i][j]];
        }
        cjr = (nl0 - gl0) % 31 + 1;
        cjy = (nl0 - gl0 > 30) ? 2 : 1;
        jq = tg[(dy + 6) % 10] + dz[dy % 12];
        jh = tg[(dy + 7) % 10] + dz[(dy + 1) % 12];
        s1 = "<title>查询结果</title><body bgcolor=#FFFFFF text=#ff0000><center>" + "<table width=400><tr><td><font size=4>您查询的结果如下:<p>公历：" + y + "年";
        s2 = "<br>春节：" + cjy + "月" + cjr + "日<br>节前：" + jq + "年<br>节后：" + jh + "年<br>";
        s3 = "要查询生辰八字，请输入时。";
        s4 = "</font></td></tr></table></center></body>";
        m = form.m;
        d = form.d;
        h = form.h;
        if (m == "" || d == "") {
            document.write(s1, s2, "<br>", "进一步查询，请输入月和日。<br>", s3, s4);
            document.close();
        } else if (m > 12 || m < 1)
            alert("月应在1与12之间。" + re);
        else if (d > 31 || d < 1)
            alert("日应在1与31之间。" + re);
        else if ((m == 4 || m == 6 || m == 9 || m == 11) && d > 30)
            alert(m + "月只有30天。" + re);
        else if (y % 4 != 0 && m == 2 && d > 28)
            alert(y + "年是平年，2月只有28天。" + re);
        else if (m == 2 && d > 29)
            alert(y + "年是闰年，2月只有29天。" + re);
        else if (h > 23 || h < 0)
            alert("时应在0与23之间。" + re);
        else {
            if (form.h == "") h = 0;
            sum = (Date.UTC(y, m - 1, d, h) - Date.UTC(1901, 1, 18, 23)) / 1000;
            sumd = Math.floor(sum / 86400);
            day = (Math.floor((sum - 1800) / 86400) + 51) % 7;
            xq = (day == 0) ? "日" : sz[day - 1];
            tgr = (sumd + 54) % 10;
            dzr = (sumd + 52) % 12;
            gzr = tg[tgr] + dz[dzr];
            dzs = Math.floor((h * 1 + 1) / 2) % 12;
            tgs = ((tgr % 5) * 2 + dzs) % 10;
            gzs = tg[tgs] + dz[dzs];
            for (i = 0; ms[i][120] <= sumd; i++);
            k = (i == 0) ? 0 : ms[i - 1][120];
            p = i * 120;
            for (j = 0; j < 120; j++) {
                k += ly[ms[i][j]];
                p++;
                if (k > sumd) break;
            }
            if (sumd + 30 < 0) {
                ri = 59 + sumd;
                p = -1;
            } else if (sumd < 0) {
                ri = 30 + sumd;
                p = 0;
            } else
                ri = sumd + ly[ms[i][j]] - k;
            yue = ((p + 11) % 12 == 0) ? "正" : sz[(p + 11) % 12];
            mij = ms[i][j];
            if ((mij == 2 || mij == 3) && ri > 28) {
                ri -= 29;
                yue = "闰" + yue;
            } else if ((mij == 4 || mij == 5) && ri > 29) {
                ri -= 30;
                yue = "闰" + yue;
            }
            ri = ((ri < 10) ? "初" : "") + sz[ri];
            tgn = Math.floor((p - 1) / 12 + 7) % 10;
            dzn = Math.floor((p - 1) / 12 + 1) % 12;
            gzn = tg[tgn] + dz[dzn];
            tgy = (p + 5) % 10;
            dzy = (p + 1) % 12;
            gzy = tg[tgy] + dz[dzy];
            tn = tw[tgn];
            dn = dw[dzn];
            ty = tw[tgy];
            dy = dw[dzy];
            tr = tw[tgr];
            dr = dw[dzr];
            ts = tw[tgs];
            ds = dw[dzs];
            s5 = m + "月" + d + "日（星期" + xq + "）";
            s6 = "<br>农历：" + gzn + "年" + yue + "月" + ri + "日";
            s7 = "生肖：" + sx[dzn] + "<p>"
            // if (form.h == "")
                // window.scbz = [s1, s5, s6, s2, "干支：", gzn, "年", gzy, "月", gzr, "日<br>", s7, s3, s4].join(' ');
            // else
                window.scbz = [// s1, s5, h, "点", s6, dz[dzs], "时", s2,
                    gzn, "　", gzy, "　", gzr, "　", gzs, 
                    // "五行：", w[tn], w[dn], "　", w[ty], w[dy], "　", w[tr], w[dr], "　", w[ts], w[ds], "<br>",
                    // "方位：", f[tn], f[dn], "　", f[ty], f[dy], "　", f[tr], f[dr], "　", f[ts], f[ds], "<br>", s7, s4
                    ].join(' ');
        }
    }
}

function insertSCBZ() {
	var template = $('<span>八字:</span><span style="color:rgb(253, 3, 3);">'+ window.scbz +'</span>');
	$('#scbz').append(template);
}

for (var i=0; i<ejs.data.twelveGongs.length; i++) {
	var gong = ejs.data.twelveGongs[i];
	if (gong.gongName.indexOf('命') != -1) {
		setCentDom(null, i);	
	}
}


inq(ejs.data.inputs);
insertSCBZ();

