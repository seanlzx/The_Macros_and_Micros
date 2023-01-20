"use strict";

/* 
    in HTML ensure this hierachy
        div class="tabGroup"
            button
            div
        the innerHTML of the buttons should be the same as the id of the tab divs
*/

let tabGroupList = document.getElementsByClassName("tabGroup");

let tabButtonList = []
let tabList = []
for (let tabGroup of tabGroupList){
    tabButtonList.push(...tabGroup.querySelectorAll(":scope > button"));
    tabList.push(...tabGroup.querySelectorAll(":scope > div"));
}

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

