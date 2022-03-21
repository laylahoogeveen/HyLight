
$(document).ready(function(){
    makeClickable();
    questionsByYou();
    notifications();
    notificationRedirect();
 });

function makeClickable() {
    $('#profile_link').click(function(){
        window.location.href='/profile';
     })
}

function questionsByYou() {
    $('#your_questions_link').click(function(){
        window.location.href='/questions_by_you';
    })
}

function notifications() {
    $('#notifications_link').click(function(){
        window.location.href='/notifications';
    })
}
// question_status answer notification_redirect
function notificationRedirect() {
    $(".question_status.answer.notification_redirect").each(function(index){
        $(this).on("click", function(){
            var url = $(this).next(".hidden_text").text();
            window.location.href=url;
        });
    });
}
