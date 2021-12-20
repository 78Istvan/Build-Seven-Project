$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
    $('select').formSelect();
    $('.modal').modal();
  });
  
// delete function 
function deleteRecipe(id) {
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
// update function 
function updateRecipe(id) {
  var id=$('input.recepy-id').val(),
  base_url = new URL('/', location.href).href,
  url = base_url +"/recipe/" + id;
  console.log(base_url)

  $.ajax({    
    type: 'UPDATE',
    url: url, //- action form
    data: id,
    success: function(){
      window.location.replace("/get_cooking");
    }
  });

}

var textarea = $('#area');
$("#popup").click(function(){

   // To show it
   textarea.show();

});

