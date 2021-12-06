window.addEventListener("DOMContentLoaded", loadedHandler);

function loadedHandler() {

    let pass_reveal = document.getElementById("random_pass_reveal");

    pass_reveal.addEventListener("click", revealPass);

}

function revealPass() {

    let pass = document.getElementById("random_pass");

    pass.style.display = "block";

}