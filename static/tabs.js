"use strict";

function create_tab_event_listeners(tabGroup) {
	let btn_collection = document.querySelectorAll(`#${tabGroup} > button`);
	let div_collection = document.querySelectorAll(`#${tabGroup} > div`);

	for (let btn of btn_collection) {
		btn.className = "tabButton";

		btn.addEventListener("click", (event) => {
			if (event.target.className == "tabButton") {
				for (let div of div_collection) {
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

	for (let div of div_collection) {
		div.className = "tab";
	}
}

create_tab_event_listeners("tabGroup1");
