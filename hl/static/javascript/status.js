$(document).ready(function() {
    $('div.question_status:contains(pending)').css('background-color', '#f98d8d');
    $('div.question_status:contains(answered)').css('background-color', '#9dd4a8');
    $('div.question_status:contains(in progress)').css('background-color', '#f9e0a3');
    answerQuestion();
    modifyQuestion();
    hideQuestion();
    selectMe();
    defaultValue();
    
    // $('.user_info_hover').hover( function() { $('#layla2').toggle(); } );
    
});

$(document).ready(function (e) {
    $(".questions_ava").hover(function (e) {
        $(this).prev('.user_info_hover').show();
    }, function (e) {
        $(this).prev('.user_info_hover').hide();
    });
});



function answerQuestion() {
    $(".question_status.answer").on('click', function(event){
        $(this).parent().next('.answer_popup').css('display', 'grid');
        $("#panel").show();
        // toggleClass('expand_descr' );
    });

}

function selectMe() {
    var span = $(".selectme");
    $(span).find("input:radio").prop('checked', true);
}

function defaultValue() {
    $(".default_value").each(function(){
        $(this).val($(this).next('.hidden_text').text());
    })
}

function modifyQuestion() {
    $(".question_status.change").on('click', function(event){
        $(this).prev('.change_question_popup').css('display', 'grid');

        $("#panel").show();
        // toggleClass('expand_descr' );
    });

}

function hideQuestion() {
    $(".close_popup").on('click', function(event){
        $(this).parent().hide(100);
        $("#panel").fadeOut("fast");
    });

}


// function showDescription() {
// $(".question_status.answer").on('click', function(event){
//     $(this).prev().css('border', 'green 2px solid');
//     // toggleClass('expand_descr' );
// });

// }
