function renderStarExplanation(starExplanation) {
  var masterDiv = $('.edit-div');
  var majorStars = [];
  var minorStars = [];
  for (var star in starExplanation) {
    console.log('star:', star);
    var expObj = starExplanation[star];
    if (expObj['zhu'] == 1) {
      // major star
      var subMajorEditDiv = $('<div class="sub-major-edit-div"><h3>'+ star +'</h3></div>');
      for (var gong in expObj['explanation']) {
        var subEditDiv = $('<div class="indent"><div class="sub-edit-div" data-star-name="' + star + '" data-gong-name="' + gong + '"><label>'+ gong +'</label><input type="text" name="'+ gong +'" class="sub-edit-input" size="40"></input></div></div>');
        subEditDiv.find('input').val(expObj['explanation'][gong]);
        subMajorEditDiv.append(subEditDiv);
      }
      majorStars.push(subMajorEditDiv);
    }
    else {
      // minor star
      var subEditDiv = $('<div class="sub-edit-div" data-star-name="' + star + '"><label>'+ star +'</label><input type="text" name="'+ star +'" class="sub-edit-input" size="40"></input></div>');
      subEditDiv.find('input').val(expObj['explanation']);
      minorStars.push(subEditDiv);
    }
  }
  masterDiv.append(majorStars);
  masterDiv.append(minorStars);
  $('.login-div').hide();
  $('.edit-div').show();
}


$('#login-form').submit(function(e) {
    console.log($(this).serializeArray());
    $.ajax('/jiexi', {
        data: {
          password: $(this).serializeArray()[0].value
        },
        method: 'POST',
        success: function(res) {
          console.log(res);
          window.starExplanation = res;
          renderStarExplanation(res);
        },
        error: function(res) {
          console.log(res);
          alert('密码错误！');
          
        }
    });
    console.log('submit handler done');
    return false;
});

function checkInputs() {
  var subEditDivs = $('.sub-edit-div');
  var inputs = subEditDivs.find('input');
  console.log(inputs);
  var valid = true;
  inputs.each(function(index, element) {
    var star = ($(element).parent().attr('data-star-name'));
    var gong = ($(element).parent().attr('data-gong-name'));
    var exp = ($(element).val());
    if (exp.indexOf('"') != -1) {
      alert('在'+ star + gong +'释义中包含双引号。请重新检查输入。');
      valid = false;
      return false;
    }
    if (exp.indexOf('\n') != -1) {
      alert('在'+ star + gong +'释义中包含回车。请重新检查输入。');
      valid = false;
      return false;
    }
  });
  if (!valid) {
    return false;
  }
  else {
    inputs.each(function(index, element) {
      var star = ($(element).parent().attr('data-star-name'));
      var gong = ($(element).parent().attr('data-gong-name'));
      var exp = ($(element).val());
      if (!gong) {
        window.starExplanation[star]['explanation'] = exp;
      }
      else {
        window.starExplanation[star]['explanation'][gong] = exp;
      }
    });
    return true;
  }
  
}

$('.submit-edit').click(function(e) {
  if (!checkInputs()) {
    return;
  }
  alert('正在提交编辑内容...');
  $.ajax('/jiexi', {
    method: 'PUT',
    data: window.starExplanation,
    success: function(res) {
      alert('保存编辑成功！');
    },
    error: function(res) {
      alert('保存编辑失败...请联系维护人员wangboyangwby@gmail.com');
    }
  });
});
console.log('handler done');
