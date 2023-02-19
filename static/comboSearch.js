function comboSearch(searchInput, container_id, foodForm_id) {
	searchInput = document.querySelector(`#${searchInput}`);

	$.ajax({
		url: "/load_comboSearch",
		type: "get",
		data: {
			search: searchInput.value,
			container_id: container_id,
			foodForm_id: foodForm_id,
		},
		success: function (response) {
			$(`#${container_id}`).html(response);
		},
		error: function (xhr) {
			console.log(xhr);
		},
	});
}

function combo_loadForm(combo_id, container_id, foodForm_id) {
	$.ajax({
		url: "/combo_loadForm",
		type: "get",
		data: { 
            id: combo_id, 
            foodForm_id:foodForm_id 
        },
		success: function (response) {
			$(`#${container_id}`).html(response);
		},
        error: function(xhr){
            console.log(xhr)
        }
	});
}

function comboForm_addAll(foodForm_id, comboElement_id){
    let span_data_list = document.querySelectorAll(`#${comboElement_id} span`)

    for (let span of span_data_list){
        console.log(span)
        comboForm_add(
            foodForm_id,
            span.getAttribute("data-food-id"),
            span.getAttribute("data-food-name"),
            span.getAttribute("data-food-quantity")
        )
    }
}

function comboForm_add(foodForm_id, food_id, food_name, food_quantity){
    let id = generateIdNum();

    let foodFormat = 
    `
    <div id="food${id}">
        <b>${food_name}</b>
        <input
            value="${food_id}"
            placeholder="foodId"
            name="foodId"
            title="foodId"
            hidden
            readonly
        />
        <input
            class="foodQuantity"
            onchange="this.setAttribute('value', this.value)"
            placeholder="quantity (grams)"
            type="number"
            name="foodQuantity"
            step="1"
            value="${food_quantity}"
            required
        />
        <button onclick="removeParentElement(this)">x</button>
    </div>
    `
    
	document.getElementById(foodForm_id).innerHTML =
    document.getElementById(foodForm_id).innerHTML + foodFormat;
}