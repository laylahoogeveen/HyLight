$(document).ready(function() {
    defaultValue();
    selectMe();
    answerHeight();
});


function defaultValue() {
    $(".default_value.availability").each(function(){
        $(this).val($(this).next('.hidden_text').text());
    })
}

function selectMe() {

    var span = $(".selectme");
    $(span).find("input:checkbox").prop('checked', true);
}





