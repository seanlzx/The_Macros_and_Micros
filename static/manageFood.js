"use strict";

document.querySelector("#manageFoodSearchButton").addEventListener("click", ()=>{
    let manageFoodSearch = document.querySelector("#manageFoodSearch")

    $.ajax({
        url:"/manageFood_searchResults",
        type: "get",
        data: {search: manageFoodSearch.value},
        success: function(response){
            $("#manageFoodResults").html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
})

function manageFoodLoadEditor(id){
    $.ajax({
        url:"/manageFoodLoadEditor",
        type: "get",
        data: {id: id},
        success: function(response){
            $("#manageFoodResults").html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
}

function editor_mg2g(id){
    let n = document.getElementById(`editor_nutrient${id}`).value;
    document.getElementById(`editor_nutrient${id}`).value = n*0.001;
    document.getElementById(`editor_unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`editor_unit${id}`).innerHTML = 'grams';
    document.getElementById(`editor_undo_mg2g${id}`).style.display = 'inline';
}
function editor_μg2g(id){
    let n = document.getElementById(`editor_nutrient${id}`).value;
    document.getElementById(`editor_nutrient${id}`).value = n*0.000001;
    document.getElementById(`editor_unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`editor_unit${id}`).innerHTML = 'grams';
    document.getElementById(`editor_undo_μg2g${id}`).style.display = 'inline';
}

function editor_undo_mg2g(id){
    let n = document.getElementById(`editor_nutrient${id}`).value;
    document.getElementById(`editor_nutrient${id}`).value = n*1000;
    document.getElementById(`editor_undo_mg2g${id}`).style.display = 'none';
    document.getElementById(`editor_unitConvertBtns${id}`).style.display = 'inline';
}

function editor_undo_μg2g(id){
    let n = document.getElementById(`editor_nutrient${id}`).value;
    document.getElementById(`editor_nutrient${id}`).value = n*1000000;
    document.getElementById(`editor_undo_μg2g${id}`).style.display = 'none';
    document.getElementById(`editor_unitConvertBtns${id}`).style.display = 'inline';
}