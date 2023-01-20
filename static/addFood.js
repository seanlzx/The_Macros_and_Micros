function mg2g(id){
    let n = document.getElementById(`nutrient${id}`).value;
    document.getElementById(`nutrient${id}`).value = n*0.001;
    document.getElementById(`unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`unit${id}`).innerHTML = 'grams';
    document.getElementById(`undo_mg2g${id}`).style.display = 'inline';
}
function μg2g(id){
    let n = document.getElementById(`nutrient${id}`).value;
    document.getElementById(`nutrient${id}`).value = n*0.000001;
    document.getElementById(`unitConvertBtns${id}`).style.display = 'none';
    document.getElementById(`unit${id}`).innerHTML = 'grams';
    document.getElementById(`undo_μg2g${id}`).style.display = 'inline';
}

function undo_mg2g(id){
    let n = document.getElementById(`nutrient${id}`).value;
    document.getElementById(`nutrient${id}`).value = n*1000;
    document.getElementById(`undo_mg2g${id}`).style.display = 'none';
    document.getElementById(`unitConvertBtns${id}`).style.display = 'inline';
}

function undo_μg2g(id){
    let n = document.getElementById(`nutrient${id}`).value;
    document.getElementById(`nutrient${id}`).value = n*1000000;
    document.getElementById(`undo_μg2g${id}`).style.display = 'none';
    document.getElementById(`unitConvertBtns${id}`).style.display = 'inline';
}