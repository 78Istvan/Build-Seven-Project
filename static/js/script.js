$(document).ready(function(){
    $('.sidenav').sidenav({edge: "right"});
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
function deleteRecipe(id) {
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

function ratingLike() {
  console.log("hello")
}