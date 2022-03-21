
$(document).ready(function() {
    omw();
});
function omw() {
    // $(".default_value").each(function(){
    //     $(this).val($(this).next('.hidden_text').text());
    // })
    $(".omw").each(function(){
        // $(this).css('background', 'red');
        $(this).children('textarea').css('background', 'yellow');
        $(this).children('textarea').val($(this).children('.hidden_text').text().trim());
        // $(this).find('input').css('background', 'yellow');
        // $(this).first('p').val('test');
    })
}