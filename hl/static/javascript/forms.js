window.onload = function() {
    makeSkillList();
    checkSkills();
    // printSkills();
  }


const user_skills = [];
var list = document.getElementsByClassName("user_skills");

const allInputs = document.getElementsByTagName("label");

function makeSkillList(){
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
        }
        

    }
}

// function printSkills() {
//     for (var i = 0, max = user_skills.length; i < max; i++){
//         console.log(user_skills[i]);
//     }
// }