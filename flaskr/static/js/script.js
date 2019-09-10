// <!-- 获取当前选择的project name -->
$('#inputGroupSelect01').change(function(){
  console.log($('#inputGroupSelect01 option:selected').text());
});


// <!-- 显示当前所选文件的名称 -->
$("#inputGroupFile04").change(function(e){
  var fileName = $('#inputGroupFile04').val().split('\\').pop();
  $('.custom-file-label').text(fileName);
});

// <!-- 导入用例 -->
$('#importcase').submit(function(e){
  e.preventDefault();
  var formData = new FormData(this);

  $.ajax({
    url: '/import',
    type: 'POST',
    data: formData,
    success: function(data){
      // 文件上传成功后，建立socket连接

      startSocket();

      let i = 0;
      var refreshicon = '<i class="fa fa-spinner fa-spin"></i>';
      $.each(data, function(index, value){
        let dt = 'title' + i;
        $('table').append('<tr data-toggle="collapse" data-target=".' + dt + '" aria-expanded="true"'+'>' + '<th scope="row">' + i + '</th>' + '<td>' + value.title + '</td>'+'<td>'+'</td>'+ '<td>'+'</td>' +'<td>'+refreshicon+'</td>' + '</tr>');
        $.each(value.steps, function(idx, steps){
          $('table').append('<tr class="collapse ' + dt + '">' + '<th scope="row">' + '</th>' + '<td></td>' +  '<td>' + steps.step + '</td>'+ '<td>' + steps.result + '</td>'+ '<td>'+refreshicon+'</td>'+'</tr>');
          // $('table').append('<tr>' + '<th scope="row">' + i + '</th>' + '<td>' + value.title + '</td>' +  '<td>' + steps.step + '</td>'+ '<td>' + steps.result + '</td>'+ '</tr>');
        });
        i = i + 1;
      });
    },
    cache: false,
    contentType: false,
    processData: false
  });

});


// $(function(){
//   setInterval("getLog()", 3000);
// });

// function getLog(){
//   $.getJSON('/rest/api/logs', 
//   function(data){
//     $('#exampleFormControlTextarea1').text(data.logs);
//   });
// }


function startSocket(){
  namespace = '/cases';

  var socket = io(namespace);
  var i = 1;

  socket.on('connect', function(){
    socket.emit('my_event', {data: 'I\'m connected'});
  });

  socket.on('my_response', function(msg, cb){
    var tb = document.getElementById('table');
    tb.rows[i++].cells[4].innerHTML = '<i class="fa fa-check"></i>';
  });

  socket.on('disconnect', function(){
    socket.close()
  });

}
