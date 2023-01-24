"use strict";
function addCombo_AddFood(){
    let id = generateIdNum();

    let foodFormat = 
    `
    <div id='food${id}'>
        <input id='foodNameInput${id}' onchange='valueUpdate("foodNameInput${id}")' placeholder="food" list="foodList" name="food"/>
        <input id='foodQuantityInput${id}' onchange='valueUpdate("foodQuantityInput${id}")'  placeholder="quantity (grams)" type='number' name="foodQuantity" step='1'>
        <button onclick='removeElement("food${id}")' type="button">x</button>
    </div>
    `

    document.getElementById('comboFoodForm').innerHTML = document.getElementById('comboFoodForm').innerHTML + foodFormat 
}