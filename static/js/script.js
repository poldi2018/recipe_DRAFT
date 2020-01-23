// variables
var add_recipe_Btn_Active=false;
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

//function for onchange event of file input field to convert selected file into base64
function encodeImgtoBase64(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function () {
    // writing reader result without mime type information to hidden textarea field to use with form.get method in python    
    $("#base64file").text(reader.result.split(',')[1]);
    }
    reader.readAsDataURL(file);
  }


  function ImageNameValidator() {
    var enteredFilename = $('#fileinputfield').val();
    if (enteredFilename.length!=0) {
        add_recipe_Btn_Active=true;
    }
    if ($('#fileinputfield').val().length == 0) {
      $('.popupImageValidator').html(`Please select an JPEG or JPG.`);
      ImageValidator();

    }


  }

  function popupCheckImageName() {
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

  function processNames() {
    namePlayer1 = $('#nameFieldPlayer1Form').val();
    $('.namePlayer1Field').html(namePlayer1 + ": ");
    namePlayer2 = $('#nameFieldPlayer2Form').val();
    $('.namePlayer2Field').html(namePlayer2 + ": ");
    $('#enterPlayersModal').css("opacity", "0.0");
    setTimeout(function() {
        $('#enterPlayersModal').css("transform", "translateZ(-10px)").css("z-index", "-1");
    }, 1000);
}

  // ... for save button button on registration modal
  $('#addRecipeBtn').on('touchstart click', function() {
    ImageNameValidator();
});

