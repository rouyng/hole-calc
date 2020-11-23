// Custom JS for hole-calc

// run toggleTol when page loads, so if "toleranced" is selected the fields will show after reloading the page
document.addEventListener("DOMContentLoaded", function() {
  toggleTol();
});

// function to toggle showing pin tolerance options.
function toggleTol () {
    let tolDivs = document.getElementsByClassName("tol-params")
    for (let f of tolDivs) {
            if (document.getElementById("tol").checked) {
                f.style.visibility = "visible";
            } else {
                f.style.visibility = "hidden";
            }
    }
}