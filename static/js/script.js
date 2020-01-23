// variables
var add_recipe_Btn_Active=False;
var fieldcount=1;
function increase_ingredientfield()
{ 
    var ingredientfield="ingredient"+fieldcount;
    return ingredientfield;
}

function addField()
{ $(".testdiv").append("<div class='row'><input id='ingredient' name='formtestfield' type='text' class='validate'><label for='testfield'></label></div><p></p>");
$('#ingredient').attr('id', increase_ingredientfield()).attr('name', increase_ingredientfield());
fieldcount++;}

/*$(document).on('touchstart click', '.addfield', function() {
    $(".testdiv").append("<div class='row'><input id='ingredient' name='formtestfield' type='text' class='validate'><label for='testfield'></label></div><p></p>");
    $('#ingredient').attr('id', increase_ingredientfield()).attr('name', increase_ingredientfield());
    fieldcount++;
});
*/

function encodeImgtoBase64(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function () {
    $("#base64file").text(reader.result.split(',')[1]);
    }
    reader.readAsDataURL(file);
  }


  function ImageValidator() {
    var enteredFilename = $('#fileinputfield').val();
    if (enteredFilename.length!=0) {
        add_recipe_Btn_Active=True
    }
    if ($('#fileinputfield').val().length == 0) {
      $('.popupImageValidator').html(`Please select an JPEG or JPG.`);
      ImageValidator();

    }


  }

  function popupCheckImagename() {
    $('.popupCheckImagename').css("transform", "translateZ(500px)").css("z-index", "500");

    setTimeout(function () {
        $('.popupCheckImagename').css("opacity", "1.0");
      }

      , 300);

    setTimeout(function () {
        $('.popupCheckImagename').css("opacity", "0.0");
      }

      , 2200);

    setTimeout(function () {
        $('.popupCheckImagename').css("transform", "translateZ(-10px)").css("z-index", "-1");
      }

      , 3000);

  }