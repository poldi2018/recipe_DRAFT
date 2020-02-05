// variables
var add_recipe_Btn_Active = false;
var fieldcount = 1;
var currentIngredientFieldname = "";

function generate_ingredientfield() {
    fieldcount++;
    var ingredientfield = "ingredient" + fieldcount;
    currentIngredientFieldname = ingredientfield;
    return ingredientfield;
}

function decrease_ingredientfield() {
    if (fieldcount >= 2) {
        fieldcount--;
    }
    var ingredientfield = "ingredient" + fieldcount;
    currentIngredientFieldId = "#" + ingredientfield;
    return ingredientfield;
}


function addIngredientField() {
    $("#ingredientWrapper").append("<div class='row'><input id='ingredient' name='ingredient' type='text' class='validate'><label for='ingredient'></label></div><p></p>");
    $('#ingredient').attr('id', generate_ingredientfield()).attr('name', generate_ingredientfield());
}

function removeIngredientField() {
    var tmpfield = "";
    $(currentIngredientFieldId).remove();
    fieldcount--;
    currentIngredientFieldId = "#ingredient" + fieldcount;
}

$('.addIngredientField').on('touchstart click', function () {
    addIngredientField();
});

$('.removeIngredientField').on('touchstart click', function () {
    removeIngredientField();
});



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


function validateImageName() {
    var enteredFilename = $('#fileinputfield').val();
    if (enteredFilename.length != 0) {
        add_recipe_Btn_Active = true;
    }
    if ($('#fileinputfield').val().length == 0) {
        $('.popupCheckImagename').html(`Please select an JPEG or JPG.`);
        popupCheckImageName();

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
    setTimeout(function () {
        $('#enterPlayersModal').css("transform", "translateZ(-10px)").css("z-index", "-1");
    }, 1000);
}

// ... for save button button on registration modal
$('#addRecipeBtn').on('touchstart click', function () {
    validateImageName();
});

$(document).ready(function () {
    $('select').material_select();


});

$('#showReviewsPopupBtn').on('touchstart click', function () {
    $('#reviewsPopup').css("transform", "translateX(0vw)").css("z-index", "500");
    $('#reviewsPopup').css("opacity", "1.0");
});

$('#closeReviewsPopupBtn').on('touchstart click', function () {
    $('#reviewsPopup').css("opacity", "0.0");
    setTimeout(function () {
        $('#reviewsPopup').css("transform", "translateX(-100vw)").css("z-index", "-1");
    }, 200);
});

$('#showRatePopupBtn').on('touchstart click', function () {
    $('#ratePopup').css("transform", "translateX(0vw)").css("z-index", "500");
    $('#ratePopup').css("opacity", "1.0");
});

$('#closeRatePopupBtn').on('touchstart click', function () {
    $('#ratePopup').css("opacity", "0.0");
    setTimeout(function () {
        $('#ratePopup').css("transform", "translateX(-100vw)").css("z-index", "-1");
    }, 200);   
});


function calcTotalTime() {
    let totalTime=parseInt($("#prepTime").val())+parseInt($("#cookingTime").val());
    $("#totalTime").html(totalTime+" mins");
}
