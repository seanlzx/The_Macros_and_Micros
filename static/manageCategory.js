"use strict";

document.querySelector("#manageCategorySearchButton").addEventListener("click", ()=>{
    let manageCategorySearch = document.querySelector("#manageCategorySearch")

    $.ajax({
        url:"/manageCategory_searchResults",
        type: "get",
        data: {search: manageCategorySearch.value},
        success: function(response){
            $("#manageCategoryResults").html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
})

function manageCategoryLoadEditor(id){
    $.ajax({
        url:"/manageCategoryLoadEditor",
        type: "get",
        data: {id: id},
        success: function(response){
            $("#manageCategoryResults").html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
}