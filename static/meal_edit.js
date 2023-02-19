function meal_loadEditForm(id){
    $.ajax({
        url:"/meal_loadEditForm",
        type: "get",
        data: {id: id},
        success: function(response){
            $(`#meal${id} .editor_container`).html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
}

