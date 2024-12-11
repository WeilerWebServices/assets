const form = document.getElementById("accountForm");
form.addEventListener("submit", (event) => {
	event.preventDefault();
	const username = document.getElementById("username").value;
	const email = document.getElementById("email").value;
	const password = document.getElementById("password").value;
	const age = document.getElementById("ageInput").value;
	if (username && email && password && age && age >= 21) {
		localStorage.setItem("username", username);
		localStorage.setItem("email", email);
		localStorage.setItem("password", password);
		localStorage.setItem("age", age);
		window.alert("Congratulations! Your account has been created.");
		window.location.reload();
	} else {
		alert(
			"Please provide all required information and verify you are over 21 to continue."
		);
	}
});
