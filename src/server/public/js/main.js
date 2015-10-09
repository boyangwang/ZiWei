$( ".datepicker" ).datepicker({
	dateFormat: "yy-mm-dd",
	minDate: '1930-01-01',
	maxDate: '2014-12-31',
	showButtonPanel: true,
	changeMonth: true,
	changeYear: true,
	constrainInput: true,
	defaultDate: '1970-01-01',
	yearRange: '1930:2014'
});
console.log('datepicker init done');
var Lifesub = function(a) {
	var form = $('form#ljms_FORM_3')
	
	var formData = {};
	$.each(form.serializeArray(), function(idx, val) {
		formData[val.name] = val.value; 
	}); 
	console.log(formData);
	var date = returnDateOrNull(formData['birthday']);

	if (doFormChecking(formData, date)) {
		appendExtra(form, a, date);
		form.submit();
	}
	// window.top.location.href= "/ziweipan?" + params;
}

function appendExtra(form, mode, date) {
	var modeInput = $("<input>")
               .attr("type", "hidden")
               .attr("name", "mode").val(mode);
	form.append(modeInput);
	var minInput = $("<input>")
               .attr("type", "hidden")
               .attr("name", "min").val(0);
    form.append(minInput);
    var yInput = $("<input>")
               .attr("type", "hidden")
               .attr("name", "y").val(date.getFullYear());
    var mInput = $("<input>")
               .attr("type", "hidden")
               .attr("name", "m").val(date.getMonth() + 1);
    var dInput = $("<input>")
               .attr("type", "hidden")
               .attr("name", "d").val(date.getDate());
    form.append(yInput).append(mInput).append(dInput);
}

function doFormChecking(formData, date) {
	if (formData['name'] == '') {
		alert('姓名不能为空');
	}
	else if (!isValidDate(date)) {
		alert('生日格式不匹配。请按"yyyy-mm-dd"格式输入，或从弹出菜单中选择');
	}
	else {
		return true;
	}
	return false;
}

function returnDateOrNull(dateString) {
    var d = new Date(dateString);
    return d;
}

function isValidDate(d) {
  if ( Object.prototype.toString.call(d) !== "[object Date]" )
    return false;
  return !isNaN(d.getTime());
}
