function focusAvailability(id) {
    var time = 200;
    addBlinkClass(id, 'highlighted', time);
    removeBlinkClass(id, 'highlighted', time * 2);
    addBlinkClass(id, 'highlighted', time * 3);
    removeBlinkClass(id, 'highlighted', time * 4);
    addBlinkClass(id, 'highlighted', time * 5);
    // removeBlinkClass(id, 'highlighted', time * 6);
    
}

function removeBlinkClass(id, blinkclass, time) {
    setTimeout(function() {
        jQuery(id).removeClass(blinkclass);
    }, time);
    

}

function addBlinkClass(id, blinkclass, time) {
    setTimeout(function() {
        jQuery(id).addClass(blinkclass);
    }, time);
    
}