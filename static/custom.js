// Custom JS for hole-calc

// run toggleTol when page loads, so if "toleranced" is selected the fields will show after reloading the page
document.addEventListener("DOMContentLoaded", function () {
    toggleTol();
});

// function to toggle showing pin tolerance options.
function toggleTol() {
    let tolDivs = document.getElementsByClassName("tol-params")
    for (let f of tolDivs) {
        if (document.getElementById("tol_radio-1").checked) {
            f.style.display = "inline-block";
        } else {
            f.style.display = "none";
        }
    }
}

// disable calculate button while loading result
function loading() {
    let loaders = document.getElementsByClassName('loader');
    for (let i = 0; i < loaders.length; i++) {
        loaders[i].style.visibility = 'visible';
    }
    document.getElementById('calculate').disabled = true
}

// Plausible.io analytics event tracking scripts
// add plausible() to record custom event goals in plausible.io analytics
// see https://plausible.io/docs/custom-event-goals
window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }

// Send form submit events to plausible
let buttons = document.querySelectorAll("button[data-analytics]");
for (var i = 0; i < buttons.length; i++) {
  buttons[i].addEventListener('click', handleFormEvent);
  buttons[i].addEventListener('auxclick', handleFormEvent);
}

function handleFormEvent(event) {
  event.preventDefault();
  let attributes = event.target.getAttribute('data-analytics').split(/,(.+)/);
  let events = [JSON.parse(attributes[0]), JSON.parse(attributes[1] || '{}')];
  plausible(...events);
  setTimeout(function () {
      event.target.form.submit();
  }, 150);
}