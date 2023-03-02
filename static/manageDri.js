"use strict";

document.querySelector("#manageDriSearchButton").addEventListener("click", ()=>{
	let search = document.querySelector("#manageDriSearch").value;
    $.ajax({
        url: "/manageDri_searchResults",
        type: "get",
        data: {
            search
        },
        success: function (response) {
            $("#manageDriResults").html(response);
        },
        error: function (xhr) {
            console.log(xhr);
        },
    });
})

function manageDriLoadEditor(name) {
	$.ajax({
		url: "/manageDriLoadEditor",
		type: "get",
		data: { name: name },
		success: function (response) {
			$("#manageDriResults").html(response);
		},
		error: function (xhr) {
			console.log(xhr);
		},
	});
}