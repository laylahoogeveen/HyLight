
$(document).ready(function() {
    omw();
});
function omw() {

    $(".omw").each(function(){
        $(this).children('textarea').css('background', 'yellow');
        $(this).children('textarea').val($(this).children('.hidden_text').text().trim());

    })
}