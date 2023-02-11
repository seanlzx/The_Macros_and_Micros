for (let loading_bar of document.querySelectorAll(".loading_bar")){
    let total_width = loading_bar.offsetWidth
  
    let white_bar = loading_bar.querySelector(".upon_rda")
    let red_bar = loading_bar.querySelector(".upon_ul")
    
    let actual = parseFloat(loading_bar.getAttribute("data-actual"))
    let rda = parseFloat(loading_bar.getAttribute("data-rda"))
    let ul = parseFloat(loading_bar.getAttribute("data-ul"))
    
    let white_width = total_width*(actual/rda);
    white_width < total_width || (white_width = total_width);
    white_bar.style.width = white_width + "px";

    let red_width = total_width*(actual/ul);
    red_width < total_width || (red_width = total_width);
    red_bar.style.width = red_width + "px";
}