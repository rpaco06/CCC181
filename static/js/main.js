// VarsityQ JavaScript.

// Join form: stop an impatient double tap from creating two tickets.
const joinForm = document.getElementById("join-form");
if (joinForm) {
  const button = joinForm.querySelector("button[type=submit]");
  const originalText = button.innerHTML;

  joinForm.addEventListener("submit", () => {
    button.disabled = true;
    button.textContent = "Getting your ticket…";
  });

  // If the person comes back with the browser's Back button, make the button usable again.
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      button.disabled = false;
      button.innerHTML = originalText;
    }
  });
}