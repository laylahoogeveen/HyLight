$(document).ready(function() {
    showLightColour();
    // lightOn();
});

function showLightColour() {
    $(".light_icon").each(function(){
        var colour = $(this).next(".hidden_text.light_colour").text();
        $(this).css('background', colour);
    })
}


/* Not implemented on the website in the end, commented out to avoid 
browser prompt for Bluetooth connection*/

// function findColour(button) {
//     var colour_name = $(button).parent().parent().children().children().children().children().children('.hidden_text.light_colour').text();
//         return colour_name;
// }

// function lightOn() {
//     $(".activate_light").on('click', function(event){
//         var colour = findColour($(this));
//         // connect();
//       });
// }

// function connect(colour){

//   const Serialport = require('serialport');
//   const readline = Serialport.parsers.Readline;
//   var val = 0;
//   const port = new Serialport('COM3', {
//       baudRate: 9600
//   });
//   const parse = port.pipe(new readline({ delimiter: '\r\n' }));

//   port.on('open', function() {
//       console.log('connect ');
//   });

//   port.write(colour);
//   parse.write(colour);

//   parse.on("data", (data) => {
//       console.log(data);
//   });

// }


