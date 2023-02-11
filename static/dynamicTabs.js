"use strict";

let prevTab = null;
let tabData = {};

function create_dynamicTab_event_listeners(tabGroup) {
	for (let btn of document.querySelectorAll(`#${tabGroup} .button_container button`)) {
		btn.className = "tabButton";
	}

	let url_collection = Array.from(
		document.querySelectorAll(`#${tabGroup} .button_container button`)
	);

	let url_array = url_collection.map((button) =>
		button.getAttribute("data-url")
	);

	for (let tab of url_array) {
		document
			.querySelector(`#${tabGroup} [data-url='${tab}']`)
			.addEventListener("click", (event) => {
				if (event.target.className == "tabButtonActive") {
					event.target.className = "tabButton";

					// if the prevTab is NOT null, keep the current data
					if (prevTab != null) {
						tabData[prevTab] = document.querySelector(
							`#${tabGroup} .window_container`
						).innerHTML;
					}

					document.querySelector(`#${tabGroup} .window_container`).innerHTML =
						"";

					// since no tabs are selected, nullify previous tab, so that blank HTML isnt kept in tabData
					prevTab = null;
				} else {
					for (let elt of url_collection) {
						elt.className = "tabButton";
					}
					event.target.className = "tabButtonActive";

					// if the prevTab is NOT null, keep the current data
					if (prevTab != null) {
						tabData[prevTab] = document.querySelector(
							`#${tabGroup} .window_container`
						).innerHTML;
					}

					// if there isn't any tab data, load the data from html
					if (tabData[tab] == null) {
						$.ajax({
							url: tab,
							type: "get",
							success: function (response) {
								$(`#${tabGroup} .window_container`).html(response);
							},
							error: function (xhr) {
								console.log(xhr);
							},
						});
					} else {
						let window_container = document.querySelector(
							`#${tabGroup} .window_container`
						);
						window_container.innerHTML = tabData[tab];

						// a hacky way to solve the scripts in tabData not loading
						const parser = new DOMParser();
						const doc = parser.parseFromString(tabData[tab], "text/html");

						for (let og_script of doc.querySelectorAll("script")) {
							let script = document.createElement("script");
							try {
								new Function(og_script.textContent)();
								script.src = og_script.src;
							} catch (err) {
								console.log(err);
								console.log("likely no problem, the tab probably just didn't have a script");
							}
							window_container.appendChild(script);
							window_container.removeChild(script);
						}
					}

					//declare the current tab as prevTab
					prevTab = tab;
				}
			});
	}
}

create_dynamicTab_event_listeners("dynamicTabGroup1");
