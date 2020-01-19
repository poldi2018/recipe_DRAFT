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