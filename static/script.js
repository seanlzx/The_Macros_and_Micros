"use strict";
// ensure inputs and text area placeholders
let form_inputs = document.querySelectorAll("input");
for (let i of form_inputs) {
	i.placeholder = i.name;
}

let form_text_areas = document.querySelectorAll("textarea");
for (let i of form_text_areas) {
	i.placeholder = i.name;
}

/* 
    in HTML ensure this hierachy
        div class="tabGroup"
            button
            div
        the innerHTML of the buttons should be the same as the id of the tab divs
*/

console.log();

let tabGroupList = document.getElementsByClassName("tabGroup");

let tabButtonList = []
let tabList = []
for (let tabGroup of tabGroupList){
    tabButtonList.push(...tabGroup.querySelectorAll(":scope > button"));
    tabList.push(...tabGroup.querySelectorAll(":scope > div"));
}

console.log(tabButtonList)


for (let tabButton of tabButtonList) {
    tabButton.id = `${tabButton.innerHTML}TabButton`;
    tabButton.className = "tabButton";
    tabButton.setAttribute("onclick", `tabAction(\"${tabButton.innerHTML}\")`);
}

for (let tab of tabList) {
    tab.className = "tab";
}

function tabAction(id) {
    let clickedButton = document.getElementById(`${id}TabButton`);

    // ensure the other buttons are not active
    for (let tabButton of tabButtonList) {
        if (tabButton != clickedButton) {
            tabButton.className = "tabButton";
        }
    }
    // toggles button colors
    clickedButton.className =
        clickedButton.className == "tabButton" ? "tabButtonActive" : "tabButton";

    let clickedTab = document.getElementById(id);
    // ensure the other tabs are not active
    for (let tab of tabList) {
        if (tab != clickedTab) {
            tab.className = "tab";
        }
    }

    // toggles tab display
    clickedTab.className = clickedTab.className == "tab" ? "tabActive" : "tab";
}

function mg2g(id){
    let n = document.getElementById(id).value;
    document.getElementById(id).value = n*0.001;
}

function μg2g(id){
    let n = document.getElementById(id).value;
    document.getElementById(id).value = n*0.000001;
}