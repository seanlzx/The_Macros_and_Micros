"use strict";

function create_tab_event_listeners(tabGroup) {
	let btn_collection = document.querySelectorAll(`#${tabGroup} > button[data-tab]`);
	let div_array = []
    for (let btn of btn_collection){
        div_array.push(document.querySelector(`#${tabGroup} > #${btn.getAttribute("data-tab")}`))
    }

	for (let btn of btn_collection) {
		btn.className = "tabButton";

		btn.addEventListener("click", (event) => {
            event.preventDefault()

			if (event.target.className == "tabButton") {
				for (let div of div_array) {
					div.className = "tab";
				}
                for (let btn of btn_collection){
                    btn.className = "tabButton"
                }

				event.target.className = "tabButtonActive";

				document.querySelector(
					`#${tabGroup} > #${event.target.getAttribute("data-tab")}`
				).className = "tabActive";
			} else if (event.target.className == "tabButtonActive"){
                event.target.className = "tabButton";

				document.querySelector(
					`#${tabGroup} > #${event.target.getAttribute("data-tab")}`
				).className = "tab";
            }
		});
	}

	for (let div of div_array) {      
	    div.className = "tab";
	}
}

create_tab_event_listeners("tabGroup1");
