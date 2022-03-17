$(document).ready(function() {
    showLightColour();
});

function showLightColour() {
    $(".light_icon").each(function(){
        var colour = $(this).next(".hidden_text.light_colour").text();
        $(this).css('background', colour);
    })
}
