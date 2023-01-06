'use strict'

let numbersUsed = [];

function generateIdNum(){
    let id;
	while (true) {
		id = Math.floor(Math.random() * 1000);
		if (!numbersUsed.includes(id)) break;
        else console.log('so that just happened')
	}

    return id;
}

function addFood(){
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

function addCategory(){
    let id = generateIdNum();

    let categoryFormat =
    `
    <div id='category${id}'>
        <input id='categoryInput${id}' onchange='valueUpdate("categoryInput${id}")'  placeholder="category" list="categoryList" name="category"/>
        <button onclick='removeElement("category${id}")' type="button">x</button>
    </div>
    `

    document.getElementById('categoryForm').innerHTML = document.getElementById('categoryForm').innerHTML + categoryFormat 
}

// this is to ensure the values do not dissapear if you add another element (p.s. it's dumb but before I learnt to add items dynamically I just took the innerHTML added the new item, and replaced the original innerHTML, the onchange is needed to ensure the dom's innerHTML also contained the value)
function valueUpdate(id){
    document.getElementById(id).setAttribute('value', document.getElementById(id).value)
}

function removeElement(id){
    let element = document.getElementById(id) ;
    console.log(element)
    element.remove();
}

