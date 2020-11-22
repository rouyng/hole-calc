// Custom JS for hole-calc

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