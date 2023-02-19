



function categoryParentCheck(elm, id_prefix){
    let ctp_json = document.getElementById('ctp_json').getAttribute("data-ctpJSON")
    ctp_dict = JSON.parse(ctp_json)

    // note double check in original if parentElement really does contain all the input
    let checkBoxContainer = elm.parentElement
    for (let label of checkBoxContainer.querySelectorAll(`label`)){
        label.style.backgroundColor = ""
    }

    let checkboxes = checkBoxContainer.querySelectorAll("input[name='category']")
    for (let checkbox of checkboxes){
        if(checkbox.checked){
            //double check that id is a good selector
            if (checkbox.id.replace(id_prefix,"") in ctp_dict){
                for(let parent_id of ctp_dict[checkbox.id.replace(id_prefix,"")]){
                    checkBoxContainer.querySelector(`label[for='${id_prefix}${parent_id}']`).style.backgroundColor = "#070"
                }
            }
            checkBoxContainer.querySelector(`label[for='${checkbox.id}']`).style.backgroundColor = ""
        }
    }

    // ensure a checkbox that is checked has the green highligth removed
    for (let checkbox of checkboxes){
        if(checkbox.checked){
            checkBoxContainer.querySelector(`label[for='${checkbox.id}']`).style.backgroundColor = ""
        }
    }
}

