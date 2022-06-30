var nameInput = document.getElementById('name')
var ageInput = document.getElementById('age')
function go_to_app() {
    //set_patient_info();
    eel.set_language();
    window.location.href = "app.html";
}

function start_triaging() {
    let voice_animation = document.getElementById('voice_animation');
    voice_animation.style.display = 'block';
    eel.triage()
}

eel.expose(hide_voice_animation)
function hide_voice_animation() {
    let voice_animation = document.getElementById('voice_animation');
    voice_animation.style.display = 'none';
}

// eel.expose(get_patient_info)
// function get_patient_info() {
//     let name = nameInput.value
//     let age = ageInput.value
//     let gender = document.querySelector('input[name="gender"]:checked').value

//     var info = [name, age, gender]
//     return info
// }

eel.expose(get_language)
function get_language() {
    let language = document.querySelector('input[name="lang"]:checked').value
    return language
}

// function set_patient_info() {
//     eel.set_patient_info()
// }
