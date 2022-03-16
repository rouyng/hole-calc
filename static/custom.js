// Custom UI JS for hole-calc

// run toggleTol when page loads, so if "toleranced" is selected the fields will show after reloading the page
document.addEventListener("DOMContentLoaded", function () {
    toggleTol();
});

// function to toggle showing pin tolerance options.
function toggleTol() {
    if (document.querySelector(".calc#threepin")) {
        let tolDivs = document.getElementsByClassName("tol-params")
        for (let f of tolDivs) {
            if (document.getElementById("tol_radio-1").checked) {
                f.style.display = "inline-block";
            } else {
                f.style.display = "none";
            }
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