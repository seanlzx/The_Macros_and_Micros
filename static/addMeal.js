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

function addMealAddFood() {
	let id = generateIdNum();

	// let foodFormat =
	// `
	// <div id='food${id}'>
	//     <input id='foodNameInput${id}' onchange='valueUpdate("foodNameInput${id}")' placeholder="Search Foods" list="foodList" name="Search Foods"/>
	//     <input id='foodQuantityInput${id}' onchange='valueUpdate("foodQuantityInput${id}")'  placeholder="quantity (grams)" type='number' name="foodQuantity" step='1'>
	//     <button onclick='removeElement("food${id}")' type="button">x</button>
	// </div>
	// `

    let foodFormat = 
    `
    <div id="food${id}">
        <input class='foodSearchInput' onchange="this.setAttribute('value', this.value)" type="text" placeholder="food" list="foodList" name="food"/>
        <button onclick='searchForFood(this)' type="button">search</button>
        <button onclick="removeParentElement(this)">x</button>
        <div class="result_container"></div>
    </div>
    `

	document.getElementById("foodForm").innerHTML =
		document.getElementById("foodForm").innerHTML + foodFormat;
}

function searchForFood(elm) {
    let id = elm.parentElement.id

	let value = elm.parentElement.querySelector(".foodSearchInput").value
    console.log({value})

	$.ajax({
		url: "/addMeal_addFood_searchResults",
		type: "get",
		data: { search: value },
		success: function (response) {
			$(`#${id} .result_container`).html(response);
		},
		error: function (xhr) {
			console.log(xhr);
		},
	});
}

function addMeal_addFood_Selected(id, elm_id){
    console.log({id, elm_id})
    $.ajax({
        url:"/addMeal_addFood_selected",
        type: "get",
        data: {id: id},
        success: function(response){
            $(`#${elm_id}`).html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
}
