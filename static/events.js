// Plausible.io analytics event tracking scripts
// add plausible() to record custom event goals in plausible.io analytics
// see https://plausible.io/docs/custom-event-goals
window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }

// Send form submit events to plausible
let buttons = document.querySelectorAll("input[dataanalytics]");
for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', handleFormEvent);
    buttons[i].addEventListener('auxclick', handleFormEvent);
}

function handleFormEvent(event) {
  event.preventDefault();
  let attributes = event.target.getAttribute('dataanalytics').split(/,(.+)/);
  let events = [JSON.parse(attributes[0]), JSON.parse(attributes[1] || '{}')];
  plausible(...events);
  setTimeout(function () {
      event.target.form.submit();
  }, 150);
}