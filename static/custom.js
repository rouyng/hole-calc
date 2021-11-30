// Custom JS for hole-calc

// run toggleTol when page loads, so if "toleranced" is selected the fields will show after reloading the page
document.addEventListener("DOMContentLoaded", function () {
    toggleTol();
    const form_analytics = document.querySelector("form[data-analytics]");
    form_analytics.addEventListener('submit', registerAnalyticsEvent);
});

// add plausible() to record custom event goals in plausible.io analytics
// see https://plausible.io/docs/custom-event-goals
window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }



function registerAnalyticsEvent(event) {
    plausible(event.target.getAttribute('data-analytics'));
}

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

function loading() {
    let loaders = document.getElementsByClassName('loader');
    for (let i = 0; i < loaders.length; i++) {
        loaders[i].style.visibility = 'visible';
    }
    document.getElementById('calculate').disabled = true
}

