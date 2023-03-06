"use strict";

function mf_searchForFood(elm) {
	// check that nutrient_for_sorting field is !(required and empty)
	let nutrient_for_sorting = document.querySelector(
		"input[name='nutrient_for_sorting']"
	);

	let manageFoodSearch = document.querySelector("#manageFoodSearch").value;
	let username = elm.parentElement.querySelector(
		"input[name='username']"
	).value;
	let order =
		elm.parentElement.querySelector("input[name='order'][checked]").value ||
		"newest";
	let categories = Array.from(
		elm.parentElement.querySelectorAll("input[name='categories']")
	)
		.filter((i) => i.checked)
		.map((i) => i.value);
	let combos = Array.from(
		elm.parentElement.querySelectorAll("input[name='combos']")
	)
		.filter((i) => i.checked)
		.map((i) => i.value);
	let nutrients = Array.from(
		elm.parentElement.querySelectorAll("input[name='nutrients']")
	)
		.filter((i) => i.checked)
		.map((i) => i.value);
	let keywords = elm.parentElement.querySelector(
		"input[name='keywords']"
	).value;

	// this is necessary to prevent value from being submitted if it's not required
	let nutrient_for_sorting_value = "";
	if (nutrient_for_sorting.required)
		nutrient_for_sorting_value = nutrient_for_sorting.value;

	let nutrient_array = JSON.parse(
		document.querySelector("#hacky-nutrient").getAttribute("data-nutrientList")
	);

	// if nutrient_for_sorting.required than send it

	if (
		!nutrient_for_sorting.required ||
		(nutrient_for_sorting.value &&
			nutrient_array.includes(nutrient_for_sorting.value))
	) {
		$.ajax({
			url: "/manageFood_searchResults",
			type: "get",
			data: {
				search: manageFoodSearch,
				username,
				order,
				categories,
				combos,
				keywords,
				nutrients,
				nutrient_for_sorting_value: nutrient_for_sorting_value,
			},
			success: function (response) {
				$("#manageFoodResults").html(response);
			},
			error: function (xhr) {
				console.log(xhr);
			},
		});
	} else {
		alert(
			"You have selected an order by nutrient option, please enter a valid nutrient"
		);
	}
}

function manageFoodLoadEditor(id) {
	$.ajax({
		url: "/manageFoodLoadEditor",
		type: "get",
		data: { id: id },
		success: function (response) {
			$("#manageFoodResults").html(response);
		},
		error: function (xhr) {
			console.log(xhr);
		},
	});
}

function editor_mg2g(id) {
	let n = document.getElementById(`editor_nutrient${id}`).value;
	document.getElementById(`editor_nutrient${id}`).value = n * 0.001;
	document.getElementById(`editor_unitConvertBtns${id}`).style.display = "none";
	document.getElementById(`editor_unit${id}`).innerHTML = "grams";
	document.getElementById(`editor_undo_mg2g${id}`).style.display = "inline";
}
function editor_μg2g(id) {
	let n = document.getElementById(`editor_nutrient${id}`).value;
	document.getElementById(`editor_nutrient${id}`).value = n * 0.000001;
	document.getElementById(`editor_unitConvertBtns${id}`).style.display = "none";
	document.getElementById(`editor_unit${id}`).innerHTML = "grams";
	document.getElementById(`editor_undo_μg2g${id}`).style.display = "inline";
}

function editor_undo_mg2g(id) {
	let n = document.getElementById(`editor_nutrient${id}`).value;
	document.getElementById(`editor_nutrient${id}`).value = n * 1000;
	document.getElementById(`editor_undo_mg2g${id}`).style.display = "none";
	document.getElementById(`editor_unitConvertBtns${id}`).style.display =
		"inline";
}

function editor_undo_μg2g(id) {
	let n = document.getElementById(`editor_nutrient${id}`).value;
	document.getElementById(`editor_nutrient${id}`).value = n * 1000000;
	document.getElementById(`editor_undo_μg2g${id}`).style.display = "none";
	document.getElementById(`editor_unitConvertBtns${id}`).style.display =
		"inline";
}

function mf_check_checkbox_neighbor(span) {
	let checkbox = span.parentElement.querySelector("input[type='checkbox']");

	if (checkbox.checked) {
		checkbox.checked = false;
		span.className = "div_checkbox";
	} else {
		checkbox.checked = true;
		span.className = "div_checkbox_checked";
	}
}

let mf_nutrient_for_sorting_text = document.querySelectorAll(
	".nutrient_for_sorting_text"
);

function mf_check_radio_neighbor(span) {
	let thisRadio = span.parentElement.querySelector("input[type='radio']");
	let grandPaSpan = span.parentElement.parentElement;

	if (!thisRadio.checked) {
		thisRadio.checked = true;
		span.className = "div_checkbox_checked";
		thisRadio.setAttribute("checked", "");
	}

	for (let radio of grandPaSpan.querySelectorAll("input[type='radio']")) {
		if (!radio.checked) {
			radio.parentElement.querySelector("span").className = "div_checkbox";
			radio.removeAttribute("checked");
		}
	}

	// the below code is related to nutrient sorting stuff
	let nutrient_for_sorting = document.querySelector(
		"input[name='nutrient_for_sorting']"
	);
	let nutrient_for_sorting_span = document.querySelector(
		"#nutrient_for_sorting_span"
	);

	nutrient_for_sorting_span.style.display = "inline-block";
	nutrient_for_sorting.style.display = "none";
	nutrient_for_sorting.removeAttribute("required");
	mf_nutrient_for_sorting_text.forEach((text) => {
		text.innerHTML = "nutrient";
		text.style.color = "inherit";
	});

	for (let radio of grandPaSpan.querySelectorAll(
		"input[data-nutrient-sort-radio]"
	)) {
		if (radio.checked) {
			nutrient_for_sorting_span.style.display = "none";
			nutrient_for_sorting.style.display = "inline-block";
			nutrient_for_sorting.setAttribute("required", "");
			mf_nutrient_for_sorting_text.forEach((text) => {
				text.innerHTML = "&lt;nutrient&gt;";
				text.style.color = "green";
			});
		}
	}
}

function nutrient_for_sorting_input(input) {
	if (input.value) {
		mf_nutrient_for_sorting_text.forEach((span) => {
			span.innerHTML = input.value;
		});
	} else {
		mf_nutrient_for_sorting_text.forEach((span) => {
			span.innerHTML = "&lt;nutrient&gt;";
		});
	}
}
