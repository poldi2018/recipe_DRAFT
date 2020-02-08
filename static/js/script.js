// init

$(document).ready(function () {
    $('select').material_select();
});

// global variables
var fieldcount = 2;

function generate_ingredientfieldName() {
    var ingredientFieldname = "ingredient" + fieldcount;
    return ingredientFieldname;
}

function generate_amountfieldName() {
    var amountFieldname = "amount" + fieldcount;
    return amountFieldname;
}

$('.addIngredientField').on('touchstart click', function () {
    $("#ingredientWrapper").append("<div class='ingredientContainer'><div class='input-field'><i class='material-icons prefix'>playlist_add</i><input id='amount' name='amount' type='text' class='validate amounts' data-length='30'><label for='amount'>Amount</label></div><div class='input-field'><i class='material-icons prefix'>playlist_add</i><input id='ingredient' name='ingredient' type='text' class='validate ingredients' data-length='30'><label for='ingredient'>Ingredient</label></div></div>");
    $('#ingredient').attr('name', generate_ingredientfieldName()).attr('id', generate_ingredientfieldName());
    $('#amount').attr('name', generate_amountfieldName()).attr('id', generate_amountfieldName());
    fieldcount++;
    // addIngredientField();
});

$('.removeIngredientField').on('touchstart click', function () {
    var ingredientFieldList = document.getElementById("ingredientWrapper");
    ingredientFieldList.removeChild(ingredientFieldList.childNodes[$("#ingredientWrapper").length]);
    if (fieldcount > 1) {
        fieldcount--;
    }
    // removeIngredientField();
});

function ingredientfieldValidation() {
    let amountsArray = $('.amounts').toArray();
    let ingredientsArray = $('.ingredients').toArray();
    for (let i = 0; i < amountsArray.length; i++) {
        if (amountsArray[i].value == "") {
            return false;
        }
    }
    for (let i = 0; i < ingredientsArray.length; i++) {
        if (ingredientsArray[i].value == "") {
            return false;
        }
    }
    return true;
}

function fieldvalidation() {
    if ($('#recipetitle').val() == "") {
        alert("Please give your recipe a title")
    } else if ($('#dishType').val() == null) {
        alert("Please give your dish a type")
    } else if ($('#origin').val() == null) {
        alert("Please select the origin")
    } else if ($('#level').val() == null) {
        alert("Please select the difficulty")
    } else if ($('#prepTime').val() == "") {
        alert("Please provide a preparation timeframe")
    } else if (isNaN($('#prepTime').val())) {
        alert("Please provide number of minutes for the preparation time")
    } else if ($('#cookingTime').val() == "") {
        alert("Please provide a cooking timeframe")
    } else if (isNaN($('#cookingTime').val())) {
        alert("Please provide number of minutes for the cooking time")
    } else if ($('#fileinputfield').val() == "") {
        alert("Please provide a picture of your dish")
    } else if (ingredientfieldValidation() == false) {
        alert("Please fill all ingredient fields or remove fields not needed.")
    } else if ($('#directions').val() == "") {
        alert("Please fill in the directions")
    } else if (fieldsTooLong() == true) {
        alert("Please allow 50 characters per field and 1000 characters for directions text max.")
    } else {
        makeIngredientsStrings()
        $('#recipeForm').submit();
    }
}

function fieldsTooLong() {
    let amountsArray = $('.amounts').toArray();
    let ingredientsArray = $('.ingredients').toArray();
    for (let i = 0; i < amountsArray.length; i++) {
        if (amountsArray[i].value.length > 30) {
            return true;
        }
    }
    for (let i = 0; i < ingredientsArray.length; i++) {
        if (ingredientsArray[i].value.length > 30) {
            return true;
        }
    }
    if ($('#recipetitle').val().length > 30) {
        return true;
    } else if ($('#directions').val().length > 1000) {
        return true;
    } else {
        return false;
    }
}

function test() {
    console.log(fieldsTooLongTest());

    if (fieldsTooLongTest() == true) {
        alert("fields too long!");
    }
}

//function for onchange event of file input field to convert selected file into base64
function encodeImgtoBase64(element) {
    var file = element.files[0];
    var reader = new FileReader();
    reader.onloadend = function () {
        // writing reader result without mime type information to hidden textarea field to use with form.get() method in python    
        $("#base64file").text(reader.result.split(',')[1]);
    }
    reader.readAsDataURL(file);
}

function validateImageName(element) {
    var enteredFilename = $('#fileinputfield').val();
    if (enteredFilename.endsWith('.jpeg') || enteredFilename.endsWith('.jpg')) {
        encodeImgtoBase64(element);
    } else if (enteredFilename.endsWith('.jpeg') == false || enteredFilename.endsWith('.jpg') == false) {
        alert("Please select an JPEG or JPG.");
        $('#fileinputfield').val("");
    }
    /*
    if ($('#fileinputfield').val().length == 0) {
        $('.popupCheckImagename').html(`Please select an JPEG or JPG.`);
        popupCheckImageName();
    } 
*/
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
    if (totalTime) {
        $("#totalTime").html(totalTime + " mins");
    } else {
        $("#totalTime").html(0 + " mins");
    }
}

$('.makearray').on('touchstart click', function () {
    makeIngredientsStrings();
});

function makeIngredientsStrings() {
    let amountsArray = $('.amounts').toArray();
    let ingredientsArray = $('.ingredients').toArray();
    let amounts = "", ingredients = "";
    for (let i = 0; i < ingredientsArray.length; i++) {
    } 
    for (let i = 0; i < amountsArray.length; i++) {
        amounts = amounts + amountsArray[i].value + "#";
    }
    $('#amountsString').val(amounts);
    for (let i = 0; i < ingredientsArray.length; i++) {
        ingredients = ingredients + ingredientsArray[i].value + "#";
    }
    $('#ingredientsString').val(ingredients);
}