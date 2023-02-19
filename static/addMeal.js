"use strict";

// this function is impure, it is entirely meant to contain the codespace, so that there aren't error if the script is ran multiple times before a page reload
function getCurrentHourAndMinute() {
	// will only run if hourInput and minuteInput are empty, so that if value was changed previously, it wont change to the default

	let hourInput = document.querySelector(
		"form[action='/addMeal'] input[name='hour']"
	);
	let minuteInput = document.querySelector(
		"form[action='/addMeal'] input[name='minute']"
	);

	const d = new Date();

	if (hourInput.value == "") {
		hourInput.value = d.getHours();
	}
	if (minuteInput.value == "") {
		let minute = d.getMinutes();
		minuteInput.value = minute - (minute % 10);
	}

	document.querySelector(
		"form[action='/addMeal'] input[name=date]"
	).valueAsDate = new Date();
}

getCurrentHourAndMinute();


