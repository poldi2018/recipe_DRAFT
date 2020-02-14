// init

$(document).ready(function () {
    $('select').material_select();
    calcTotalTime();
});

// global variables
var fieldcount = $(".outerIngredientContainer").length;

$('.addIngredientField').on('touchstart click', function () {
    fieldcount++;
    var ingredientFieldname = "ingredient" + fieldcount;
    var amountFieldname = "amount" + fieldcount;
    $("#ingredientWrapper").append("<div class='outerIngredientContainer'><div class='amountContainer'><div class='input-field'><i class='material-icons prefix'>playlist_add</i><input id='amount' name='amount' type='text' class='validate amounts' data-length='30'><label for='amount'>Amount</label></div></div><div class='ingredientContainer'><div class='input-field'><i class='material-icons prefix'>playlist_add</i><input id='ingredient' name='ingredient' type='text' class='validate ingredients' data-length='30'><label for='ingredient'>Ingredient</label></div></div></div>");
    $('#ingredient').attr('name', ingredientFieldname).attr('id', ingredientFieldname);
    $('#amount').attr('name', amountFieldname).attr('id', amountFieldname);
});

$('.removeIngredientField').on('touchstart click', function () {
    if (fieldcount > 1) {
        $(".outerIngredientContainer").last().remove();
        setTimeout(function () {
            fieldcount--;
        }, 400);
    }
});
//function for onchange event of file input field to convert selected file into base64
function encodeImgtoBase64(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function () {
        // writing reader result without mime type information to hidden textarea field to use with form.get() method in python    
        $("#base64file").text(reader.result.split(',')[1]);
    };
    reader.readAsDataURL(file);
}

function calcTotalTime() {
    var totalTime = parseInt($("#prepTime").val()) + parseInt($("#cookingTime").val());
    if (totalTime) {
        if (totalTime < 60) {
            $("#totalTime").html(0 + " hrs " + totalTime + " mins");
        }
        if (totalTime >= 60)
            $("#totalTime").html(parseInt(totalTime / 60) + " hrs " + totalTime % 60 + " mins");
    } else {
        $("#totalTime").html("-");
    }
}

function makeIngredientsStrings() {
    var amountsArray = $('.amounts').toArray();
    var ingredientsArray = $('.ingredients').toArray();
    var amounts = "",
        ingredients = "";
    var i = 0;
    for (i = 0; i < amountsArray.length; i++) {
        amounts = amounts + amountsArray[i].value + "#";
    }
    $('#amountsString').val(amounts);
    i = 0;
    for (i = 0; i < ingredientsArray.length; i++) {
        ingredients = ingredients + ingredientsArray[i].value + "#";
    }
    $('#ingredientsString').val(ingredients);
}

function validateImageName(element) {
    var enteredFilename = $('#fileinputfield').val();
    if (enteredFilename.endsWith('.jpeg') || enteredFilename.endsWith('.jpg')) {
        encodeImgtoBase64(element);
    } else if (enteredFilename.endsWith('.jpeg') == false || enteredFilename.endsWith('.jpg') == false) {
        $('#resultCheckForValidFields').html("Please select an JPEG or JPG.");
        popupCheckForValidFields();
        $('#fileinputfield').val("");
    }
}

function ingredientfieldsFilled() {
    var amountsArray = $('.amounts').toArray();
    var ingredientsArray = $('.ingredients').toArray();
    var i = 0;
    for (i = 0; i < amountsArray.length; i++) {
        if (amountsArray[i].value == "") {
            return false;
        }
    }
    i = 0;
    for (i = 0; i < ingredientsArray.length; i++) {
        if (ingredientsArray[i].value == "") {
            return false;
        }
    }
    return true;
}

function fieldsTooLong() {
    var amountsArray = $('.amounts').toArray();
    var ingredientsArray = $('.ingredients').toArray();
    var i = 0;
    for (i = 0; i < amountsArray.length; i++) {
        if (amountsArray[i].value.length > 30) {
            return true;
        }
    }
    i = 0;
    for (i = 0; i < ingredientsArray.length; i++) {
        if (ingredientsArray[i].value.length > 30) {
            return true;
        }
    }
    if ($('#recipetitle').val().length > 30 || $('#directions').val().length > 1000) {
        return true;
    } else {
        return false;
    }
}

function fieldvalidation() {
    if ($('#recipetitle').val() == "") {
        $('#resultCheckForValidFields').html("Please give your recipe a title.");
    } else if ($('#dishType').val() == null) {
        $('#resultCheckForValidFields').html("Please give your dish a category.");
    } else if ($('#origin').val() == null) {
        $('#resultCheckForValidFields').html("Please select the origin.");
    } else if ($('#level').val() == null) {
        $('#resultCheckForValidFields').html("Please select the difficulty.");
    } else if ($('#prepTime').val() == "") {
        $('#resultCheckForValidFields').html("Please provide a preparation timeframe.");
    } else if (isNaN($('#prepTime').val())) {
        $('#resultCheckForValidFields').html("Please provide number of minutes for the preparation time.");
    } else if ($('#cookingTime').val() == "") {
        $('#resultCheckForValidFields').html("Please provide a cooking timeframe.");
    } else if (isNaN($('#cookingTime').val())) {
        $('#resultCheckForValidFields').html("Please provide number of minutes for the cooking time.");
    } else if ($('#fileinputfield').val() == "") {
        $('#resultCheckForValidFields').html("Please provide a picture of your dish.");
    } else if (ingredientfieldsFilled() == false) {
        $('#resultCheckForValidFields').html("Please fill all ingredient fields or remove fields not needed.");
    } else if ($('#directions').val() == "") {
        $('#resultCheckForValidFields').html("Please fill in the directions.");
    } else if (fieldsTooLong() == true) {
        $('#resultCheckForValidFields').html("Please allow 30 characters per field and 1000 characters for directions text max.");
    } else {
        $('#prepTime').val(parseInt($('#prepTime').val()));
        $('#cookingTime').val(parseInt($('#cookingTime').val()));
        makeIngredientsStrings();
        $('#recipeForm').submit();
        return;
    }
    if ($('#resultCheckForValidFields').html() != "") {
        popupCheckForValidFields();
    }
    return;
}

function popupCheckForValidFields() {
    $('#popupCheckForValidFields').css("transform", "translateX(0vw)");
    $('#popupCheckForValidFields').css("opacity", "1.0");
}

function closeCheckForValidFieldsPopup() {
    $('#popupCheckForValidFields').css("opacity", "0.0");
    setTimeout(function () {
        $('#resultCheckForValidFields').html("");
        $('#popupCheckForValidFields').css("transform", "translateX(-100vw)");
    }, 400);
}
//$('#closeCheckForValidFieldsBtn').on('touchstart click', function () {
//});

function showReviewsPopup() {
    $('#reviewsPopup').css("transform", "translateX(0vw)");
    $('#reviewsPopup').css("opacity", "1.0");
}
//$('#showReviewsPopupBtn').on('touchstart click', function () {   
//});

function closeReviewsPopup() {
    $('#reviewsPopup').css("opacity", "0.0");
    setTimeout(function () {
        $('#reviewsPopup').css("transform", "translateX(-100vw)");
    }, 400);
}
//$('#closeReviewsPopupBtn').on('touchstart click', function () {
//});

function showRatePopup() {
    $('#ratePopup').css("transform", "translateX(0vw)");
    $('#ratePopup').css("opacity", "1.0");
}
//$('#showRatePopupBtn').on('touchstart click', function () {   
//});

function sendReview() {
    if ($('#review_title').val() == "") {
        $('#resultCheckForValidFields').html("Please give your review a title.");
        popupCheckForValidFields();
    } else if ($('#level').val() == null) {
        $('#resultCheckForValidFields').html("Please select star level.");
        popupCheckForValidFields();
    } else if ($('#comment').val() == "") {
        $('#resultCheckForValidFields').html("Please provide a short feedback or suggestion");
    } else if ($('#comment').val().length > 30) {
        $('#resultCheckForValidFields').html("Please allow a maximum of 30 characters per comment.");
    }

    if ($('#resultCheckForValidFields').html() != "") {
        popupCheckForValidFields();
    } else {
        $('#ratePopup').css("opacity", "0.0");
        setTimeout(function () {
            $('#ratePopup').css("transform", "translateX(-100vw)");
        }, 400);
        $('#rateForm').submit();
    }
}
//$('#sendReviewPopupBtn').on('touchstart click', function () {   
//});

function cancelReview() {
    $('#ratePopup').css("opacity", "0.0");
    setTimeout(function () {
        $('#ratePopup').css("transform", "translateX(-100vw)");
    }, 400);
}
//$('#cancelReviewPopupBtn').on('touchstart click', function () {    
//});

function showdeleteRecipePopup() {
    $('#deletePopup').css("transform", "translateX(0vw)");
    $('#deletePopup').css("opacity", "1.0");
}
//$('#deleteRecipePopupBtn').on('touchstart click', function () {    
//});

function cancelDeleteRecipe() {
    $('#deletePopup').css("opacity", "0.0");
    setTimeout(function () {
        $('#deletePopup').css("transform", "translateX(-100vw)");
    }, 400);
}
//$('#deleteRecipePopupCancelBtn').on('touchstart click', function () {   
//});

function checkRegistrationForm() {
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    var emailToCheck=$('#email_address').val();
    if ($('#username').val() == "" || $('#email_address').val() == "" || $('#password').val() == "" || $('#password2').val() == "") {
        $('#resultCheckForValidFields').html("Please fill in all fields");
        popupCheckForValidFields();
    } else if (!$('#email_address').val().match(mailformat)) {
        $('#resultCheckForValidFields').html("Please fill in a valid email address.");
        popupCheckForValidFields();
    } else if ($('#password').val() != $('#password2').val()) {
        $('#resultCheckForValidFields').html("Passwords do not match.");
        popupCheckForValidFields();
    } else {
        $('#registrationForm').submit();
    }
}