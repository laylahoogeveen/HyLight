
$(document).ready(function(){
    makeSkillList();
    checkSkills();
 });

 $(document).ready(function () {
    $('input').change(function() {
        if (this.checked) {
        $(this).parents('li').addClass("selected_label");
        } else {
        $(this).parents('li').removeClass("selected_label");
        }
    });

});

const user_skills = [];

const allInputs = document.getElementsByTagName("label");

function makeSkillList(){
    var list = document.getElementsByClassName("user_skills");
    for (let index = 0; index < list.length; ++index) {
        var e = list[index];
        user_skills.push(e.innerHTML.trim())
    }

}

function checkSkills() {
    
    for (var i = 0, max = allInputs.length; i < max; i++){
        var name = allInputs[i].innerHTML.split('>')[1].trim();
        var checkbox = allInputs[i].getElementsByTagName("input")[0];
        // console.log(name);
        if (user_skills.includes(name) == true) {
            checkbox.checked = true;
            changeLabelEach(checkbox);
            
        }
        

    }
}

function changeLabelEach(label) { 
    if (label.checked) {
        $(label).parents('li').addClass("selected_label");
        
        } else {
        $(label).parents('li').removeClass("selected_label");
        }
}
