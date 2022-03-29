$(document).ready(function() {
    $('div.question_status:contains(pending)').css('background-color', '#f98d8d');
    $('div.question_status:contains(answered)').css('background-color', '#9dd4a8');
    $('div.question_status:contains(in progress)').css('background-color', '#f9e0a3');
    answerQuestion();
    modifyQuestion();
    hideQuestion();
    selectMe();
    defaultValue();
    changeLabel();
    
});

function changeLabel() {

    $(".remove.radio").each(function(){
            $(this).parent().addClass('btn').addClass('btn-outline-primary');
    })

    // initial value entered by user
    $(".remove.radio").each(function(){
        if($(this).is(':checked')) {
            $(this).parent('label').addClass('active');
        }
    })
    
    $(".remove.radio").on('click', function(event){
        $( this ).attr( 'checked', true );
        if($(this).is(':checked')) {

            $(this).parent('label').parent().parent().children().each(function(){
                $(this).removeClass('active');
                $(this).children().removeClass('active');
                $(this).children().children().removeClass('active');
            })

            $(this).parent('.btn.btn-outline-primary').addClass('active');
        }
    });
}

$(document).ready(function (e) {
    $(".questions_ava").hover(function (e) {
        $(this).css("cursor", "pointer");
        $(this).prev('.user_info_hover').show();
    }, function (e) {
        $(this).prev('.user_info_hover').hide();
    });
});


$(document).ready(function (a) {
    $("#question_light").hover(function (a) {
        $(this).css("cursor", "pointer");
        $('#light_explanation').show();
    }, function (a) {
        $('#light_explanation').hide();
    });
});

function answerQuestion() {
    $(".question_status.answer").on('click', function(event){
        $(this).parent().next('.answer_popup').css('display', 'grid');
        $("#panel").show();
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
    });

}

function hideQuestion() {
    $(".close_popup").on('click', function(event){
        $(this).parent().hide(100);
        $("#panel").fadeOut("fast");
    });
    $(".activate_light").on('click', function(event){
        $("#panel").fadeOut("fast");
    });

}