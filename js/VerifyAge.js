function verifyAge() {
	const ageInput = document.getElementById("ageInput");
	const errorMessage = document.getElementById("errorMessage");
	const createButton = document.getElementById("createButton");
	if (ageInput.value >= 21) {
		createButton.disabled = false;
	} else {
		createButton.disabled = true;
		errorMessage.textContent =
			"You must be at least 21 years old to create an account.";
	}
}

function showColor() {
	window.prompt(
		"You must be at least 21 years old. Verify by clicking 'Enter':"
	);
}
document.addEventListener("DOMContentLoaded", showColor);
document.getElementById("createButton").addEventListener("click", (event) => {
	event.preventDefault();
	if (age >= 21) {
		window.location.reload();
	}
});
document.getElementById("cancelButton").addEventListener("click", () => {
	window.alert("Oh well, maybe next time!");
	window.location.reload();
});
