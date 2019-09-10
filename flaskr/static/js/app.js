window.onload = function(){
    $(function(){
        $.getJSON('/rest/api/projects',
        function(data){
            $.each(data, function(_index, value){
              //  $('#result').append(value.name);
               $('#inputGroupSelect01').append('<option>'+value.name+'</option>')
            });
        });
    });
};

