"user strict";
let hourInput = document.querySelector("form[action='/addMeal'] input[name='hour']")
let minuteInput = document.querySelector("form[action='/addMeal'] input[name='minute']")

const d = new Date();

hourInput.value = d.getHours()
let minute = d.getMinutes()
minuteInput.value = minute - minute % 10  

document.querySelector("form[action='/addMeal'] input[name=date]").valueAsDate = new Date()

function addMealAddFood(){
    let id = generateIdNum();

    let foodFormat = 
    `
    <div id='food${id}'>
        <input id='foodNameInput${id}' onchange='valueUpdate("foodNameInput${id}")' placeholder="food" list="foodList" name="food"/>
        <input id='foodQuantityInput${id}' onchange='valueUpdate("foodQuantityInput${id}")'  placeholder="quantity (grams)" type='number' name="foodQuantity" step='1'>
        <button onclick='removeElement("food${id}")' type="button">x</button>
    </div>
    `

    document.getElementById('foodForm').innerHTML = document.getElementById('foodForm').innerHTML + foodFormat 
}

