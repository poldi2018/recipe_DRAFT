// variables
var add_recipe_Btn_Active = false;
var fieldcount = 2;
var currentIngredientFieldname, currentAmountFieldname = "";

function generate_ingredientfieldName() {
    var ingredientFieldname = "ingredient" + fieldcount;
    currentIngredientFieldname = ingredientFieldname;
    return ingredientFieldname;
}

function generate_amountfieldName() {
    var amountFieldname = "amount" + fieldcount;
    currentAmountFieldname = amountFieldname;
    return amountFieldname;
}

function addIngredientField() {
    $("#ingredientWrapper").append("<div class='input-field'><i class='material-icons prefix'>playlist_add</i><input id='amount' name='amount' type='text' class='validate'><label for='amount'>Amount</label></div><div class='input-field'><i class='material-icons prefix'>playlist_add</i><input id='ingredient' name='ingredient' type='text' class='validate'><label for='ingredient'>Ingredient</label></div>");
    $('#ingredient').attr('name', generate_ingredientfieldName()).attr('id', generate_ingredientfieldName());
    $('#amount').attr('name', generate_amountfieldName()).attr('id', generate_amountfieldName());
    fieldcount++;
    console.log(fieldcount);
}

function removeIngredientField() {
    var ingredientFieldList = document.getElementById("ingredientWrapper"); // Get the <ul> element with id="myList"
    ingredientFieldList.removeChild(ingredientFieldList.childNodes[$("#ingredientWrapper").length]);
    ingredientFieldList.removeChild(ingredientFieldList.childNodes[$("#ingredientWrapper").length]);
    fieldcount--;
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
    let totalTime = parseInt($("#prepTime").val()) + parseInt($("#cookingTime").val());
    $("#totalTime").html(totalTime + " mins");
}