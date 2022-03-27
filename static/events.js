// Plausible.io analytics event tracking scripts
// add plausible() to record custom event goals in plausible.io analytics
// see https://plausible.io/docs/custom-event-goals
window.plausible = window.plausible || function() { (window.plausible.q = window.plausible.q || []).push(arguments) }

// Send form submit events to plausible
let forms = document.querySelectorAll("form[dataanalytics]");
for (let i = 0; i < forms.length; i++) {
    forms[i].addEventListener('submit', handleFormEvent);
}

function handleFormEvent(event) {
  event.preventDefault();
  console.log("Handling form event")
  let attributes = event.target.getAttribute('dataanalytics').split(/,(.+)/);
  let events = [JSON.parse(attributes[0]), JSON.parse(attributes[1] || '{}')];
  plausible(...events);
  setTimeout(function () {
      event.target.submit();
  }, 150);
}