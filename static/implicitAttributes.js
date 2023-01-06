'use strict';
// ensure inputs and text area placeholders and tooltips
let form_inputs = document.querySelectorAll("input");
for (let i of form_inputs) {
	i.placeholder = i.name;
    // think of a better way to solve this problem??
    if (i.className != 'nutrient') i.title = i.name
}

let form_text_areas = document.querySelectorAll("textarea");
for (let i of form_text_areas) {
	i.placeholder = i.name;
    if (i.className != 'nutrient') i.title = i.name
}