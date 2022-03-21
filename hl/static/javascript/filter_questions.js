function hideAnswered() {

        $(".questions_sm").each(function(){
            if ($(this).is(":visible")) {
                if ($(this).children().next().next().children().next().children('.question_status.real').text().trim() == "answered") {
                    $(this).hide("slow");
                document.getElementById('hide_answered').innerHTML = "Show answered questions";
                }
            }
            else {
                if ($(this).children().next().next().children().next().children('.question_status.real').text().trim() == "answered") {
                $(this).show("slow");
                }
                document.getElementById('hide_answered').innerHTML = "Hide answered questions";

            }
        })


}

function hideInProgress() {

    $(".questions_sm").each(function(){
        if ($(this).is(":visible")) {
            if ($(this).children().next().next().children().next().children('.question_status.real').text().trim() == "in progress") {
                $(this).hide("slow");
            document.getElementById('hide_in_progress').innerHTML = "Show questions in progress";
            }
        }
        else {
            if ($(this).children().next().next().children().next().children('.question_status.real').text().trim() == "in progress") {
            $(this).show("slow");
            }
            document.getElementById('hide_in_progress').innerHTML = "Hide questions in progress";

        }
    })


}