"use strict";
function rda_mg2g(id){
    let n = document.getElementById(`rda_nutrient${id}`).value;
    document.getElementById(`rda_nutrient${id}`).value = n*0.001;
    document.getElementById(`rda_unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`rda_unit${id}`).innerHTML = 'grams';
    document.getElementById(`rda_undo_mg2g${id}`).style.display = 'inline';
}
function rda_μg2g(id){
    let n = document.getElementById(`rda_nutrient${id}`).value;
    document.getElementById(`rda_nutrient${id}`).value = n*0.000001;
    document.getElementById(`rda_unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`rda_unit${id}`).innerHTML = 'grams';
    document.getElementById(`rda_undo_μg2g${id}`).style.display = 'inline';
}

function rda_undo_mg2g(id){
    let n = document.getElementById(`rda_nutrient${id}`).value;
    document.getElementById(`rda_nutrient${id}`).value = n*1000;
    document.getElementById(`rda_undo_mg2g${id}`).style.display = 'none';
    document.getElementById(`rda_unitConvertBtns${id}`).style.display = 'inline';
}

function rda_undo_μg2g(id){
    let n = document.getElementById(`rda_nutrient${id}`).value;
    document.getElementById(`rda_nutrient${id}`).value = n*1000000;
    document.getElementById(`rda_undo_μg2g${id}`).style.display = 'none';
    document.getElementById(`rda_unitConvertBtns${id}`).style.display = 'inline';
}
function ul_mg2g(id){
    let n = document.getElementById(`ul_nutrient${id}`).value;
    document.getElementById(`ul_nutrient${id}`).value = n*0.001;
    document.getElementById(`ul_unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`ul_unit${id}`).innerHTML = 'grams';
    document.getElementById(`ul_undo_mg2g${id}`).style.display = 'inline';
}
function ul_μg2g(id){
    let n = document.getElementById(`ul_nutrient${id}`).value;
    document.getElementById(`ul_nutrient${id}`).value = n*0.000001;
    document.getElementById(`ul_unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`ul_unit${id}`).innerHTML = 'grams';
    document.getElementById(`ul_undo_μg2g${id}`).style.display = 'inline';
}

function ul_undo_mg2g(id){
    let n = document.getElementById(`ul_nutrient${id}`).value;
    document.getElementById(`ul_nutrient${id}`).value = n*1000;
    document.getElementById(`ul_undo_mg2g${id}`).style.display = 'none';
    document.getElementById(`ul_unitConvertBtns${id}`).style.display = 'inline';
}

function ul_undo_μg2g(id){
    let n = document.getElementById(`ul_nutrient${id}`).value;
    document.getElementById(`ul_nutrient${id}`).value = n*1000000;
    document.getElementById(`ul_undo_μg2g${id}`).style.display = 'none';
    document.getElementById(`ul_unitConvertBtns${id}`).style.display = 'inline';
}