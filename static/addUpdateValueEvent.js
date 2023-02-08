"use strict";
function addUpdateValueEvent(){
    let allTextInputs = document.querySelectorAll("input[type='text']");

    for (let input of allTextInputs) {
        input.addEventListener("change", (event) => {
            event.target.setAttribute("value", event.target.value);
        });
    }
    
    let allNumberInputs = document.querySelectorAll("input[type='number']");
    
    for (let input of allNumberInputs) {
        input.addEventListener("change", (event) => {
            event.target.setAttribute("value", event.target.value);
        });
    }
    
    // Note: because nutrient inputs also has the weird button to convert the values, that won't be updated when values changes
    // this is dumb but it should work, lol this is genius 😂
    let allNutrientButtons = document.querySelectorAll("span[class='nutrientSpan'] button")
    for (let button of allNutrientButtons){  
        button.addEventListener("click", event =>{
            // THE BELOW DON'T WORK, IT WORKS FOR BUTTONS "undo <insert unit>👉g" but not "mg" and "μg", probably has something to do with the fact that
            // the buttons have different nesting stuff, ANYWAYS too lazy solve so the below will suffice though it's not the best
            // event.target.parentElement.parentElement.querySelector("input").setAttribute("value", event.target.parentElement.parentElement.querySelector("input").value);
            
            // this was even dumber than before but whatever
            for (let nutrientInput of document.querySelectorAll("input[class='nutrient']")){
                nutrientInput.setAttribute("value", nutrientInput.value)
            }
        })
    } 
    
    for (let textarea of document.querySelectorAll("textarea")) {
        textarea.addEventListener("change", (event) => {
            event.target.appendChild(document.createTextNode(event.target.value));
        });
    }
    
    let allCheckboxes = document.querySelectorAll("input[type='checkbox']");
    
    for (let checkbox of allCheckboxes) {
        checkbox.addEventListener("change", (event) => {
            if (event.target.checked) event.target.setAttribute("checked", "");
            else event.target.removeAttribute("checked");
        });
    }

    let allDateInputs = document.querySelectorAll("input[type='date']");

    for (let dateInputs of allDateInputs) {
        dateInputs.addEventListener("change", (event) => {
            event.target.setAttribute("value", event.target.value);
        });
    }
    
}

addUpdateValueEvent()