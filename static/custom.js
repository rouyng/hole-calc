// Custom JS for hole-calc

// function to toggle showing pin tolerance options
const rdo = document.getElementById("tol-radio");
    rdo.onclick = function () {
    const fields = document.getElementsByClassName("tol-params");
    if (rdo.checked) {
      fields.style.visibility = "visible";
    } else {
     fields.style.display = "hidden";
    }
}