$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
  });
  
// delete function url 
function myFunction(id) {
  var id=$('input.recepy-id').val(),
  base_url = new URL('/', location.href).href,
  url = base_url +"/recipe/" + id;
  console.log(base_url)

  $.ajax({    
    type: 'DELETE',
    url: url, //- action form
    data: id,
    success: function(){
      window.location.replace("/get_cooking");
    }
  });

}