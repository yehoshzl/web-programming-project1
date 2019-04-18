// function username_check(){
  $('document').ready(function() {
    $("form").submit(function(ev){
      ev.preventDefault();
      var username = $('#username').val();
      $.get('/check?username='+username, function(response){
        if (response == 'false') {
          alert('username taken');
          document.getElementById('register').reset();
          $('#username').focus();
        }
        else
          {
            (document).getElementById('register').submit();
          }
      });
    });
  });
//}
