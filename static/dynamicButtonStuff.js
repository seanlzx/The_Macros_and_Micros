"use strict";

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

// this is to ensure the values do not dissapear if you add another element (p.s. it's dumb but before I learnt to add items dynamically I just took the innerHTML added the new item, and replaced the original innerHTML, the onchange is needed to ensure the dom's innerHTML also contained the value)
function valueUpdate(id){
    document.getElementById(id).setAttribute('value', document.getElementById(id).value)
}

function removeElement(id){
    let element = document.getElementById(id) ;
    console.log(element)
    element.remove();
}
