function addFoodSearch(foodForm_id) {
	let id = generateIdNum();
    
    let div = document.createElement("div")
    div.id = foodForm_id+"_food"+id

	document.getElementById(foodForm_id).append(div)

    $.ajax({
        url: "/foodSearch",
        type: "get",
        data:{foodForm_id, id},
        success: function (response) {
            $(`#${foodForm_id}_food${id}`).html(response);
        },
        error: function(xhr){
            console.log(xhr)
        }
    });
}

function check_checkbox_neighbor(span){
    let checkbox = span.parentElement.querySelector("input[type='checkbox']")

    if(checkbox.checked){
        checkbox.checked = false;
        span.className = "div_checkbox"
    } else {
        checkbox.checked = true;
        span.className = "div_checkbox_checked"
    }
}

function check_radio_neighbor(span){
    let thisRadio = span.parentElement.querySelector("input[type='radio']")
    let grandPaSpan = span.parentElement.parentElement

    if(!thisRadio.checked){
        thisRadio.checked = true;
        span.className = "div_checkbox_checked"
        thisRadio.setAttribute("checked", "")
    }

    for (let radio of grandPaSpan.querySelectorAll("input[type='radio']")){
        if(!radio.checked){
            radio.parentElement.querySelector("span").className = "div_checkbox"
            radio.removeAttribute("checked")
        }
    }
    
}

function searchForFood(elm) {
    let id = elm.parentElement.id

	let value = elm.parentElement.querySelector(".foodSearchInput").value
    let username = elm.parentElement.querySelector("input[name='username']").value
    let order = (elm.parentElement.querySelector("input[name='order'][checked]").value || "newest")
    let categories = Array.from(elm.parentElement.querySelectorAll("input[name='categories']")).filter(i => i.checked).map(i => i.value)
    let combos = Array.from(elm.parentElement.querySelectorAll("input[name='combos']")).filter(i => i.checked).map(i => i.value)
    let nutrients = Array.from(elm.parentElement.querySelectorAll("input[name='nutrients']")).filter(i => i.checked).map(i => i.value)
    let keywords = elm.parentElement.querySelector("input[name='keywords']").value

	$.ajax({
		url: "/addFood_searchResults",
		type: "get",
		data: { 
            search: value,
            username, 
            order,
            categories,
            combos,
            keywords,
            nutrients
        },
		success: function (response) {
			$(`#${id} .result_container`).html(response);
		},
		error: function (xhr) {
			console.log(xhr);
		},
	});
}

function addFood_Selected(id, elm_id){
    console.log({id, elm_id})
    $.ajax({
        url:"/addFood_selected",
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