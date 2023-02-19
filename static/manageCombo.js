document.querySelector("#manageComboSearchButton").addEventListener("click", ()=>{
    let manageComboSearch = document.querySelector("#manageComboSearch")

    $.ajax({
        url:"/manageCombo_searchResults",
        type: "get",
        data: {search: manageComboSearch.value},
        success: function(response){
            $("#manageComboResults").html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
})

function combo_loadEditForm(id){
    $.ajax({
        url:"/combo_LoadEditorForm",
        type: "get",
        data: {id: id},
        success: function(response){
            $("#manageComboResults").html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
}