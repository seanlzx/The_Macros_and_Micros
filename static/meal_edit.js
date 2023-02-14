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

function searchForFood(elm) {
    let id = elm.parentElement.id

	let value = elm.parentElement.querySelector(".foodSearchInput").value
    console.log({value})

	$.ajax({
		url: "/addMeal_addFood_searchResults",
		type: "get",
		data: { search: value },
		success: function (response) {
			$(`#${id} .result_container`).html(response);
		},
		error: function (xhr) {
			console.log(xhr);
		},
	});
}

function addMeal_addFood_Selected(id, elm_id){
    console.log({id, elm_id})
    $.ajax({
        url:"/addMeal_addFood_selected",
        type: "get",
        data: {id: id},
        success: function(response){
            $(`#${elm_id}`).html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    })
}

function meal_editForm_addFood(meal_id) {
	let id = generateIdNum();

    let foodFormat = 
    `
    <div id="food${id}">
        <input class='foodSearchInput' onchange="this.setAttribute('value', this.value)" type="text" placeholder="food" list="foodList" name="food"/>
        <button onclick='searchForFood(this)' type="button">search</button>
        <button onclick="removeParentElement(this)">x</button>
        <div class="result_container"></div>
    </div>
    `

	document.getElementById(`meal_editForm${meal_id}`).innerHTML =
		document.getElementById(`meal_editForm${meal_id}`).innerHTML + foodFormat;
}