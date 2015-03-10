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
	allMinorStars = allMinorStars.concat(gong.cyanStars);
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
		expP.text(expText);
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
		expP.text(expText);
		expDiv.append(expP);	
	}
}

window.goToPan = function(mode) {
	var inputs = ejs.data.inputs;
	inputs.mode = mode;
	console.log(inputs);
	var form = $('.invisible-form');
	for (var key in inputs) {
		form.append( $("<input>")
               .attr("type", "hidden")
               .attr("name", key).val(inputs[key]));
	}
	form.submit();
}

setCentDom(null, 0);