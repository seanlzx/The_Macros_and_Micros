function loading_bar_init(){
    for (let loading_bar of document.querySelectorAll(".loading_bar")) {
        let total_width = loading_bar.offsetWidth;

        let white_bar = loading_bar.querySelector(".upon_rda");
        let red_bar = loading_bar.querySelector(".upon_ul");

        let actual = parseFloat(loading_bar.getAttribute("data-actual"));
        let rda = parseFloat(loading_bar.getAttribute("data-rda"));
        let ul = parseFloat(loading_bar.getAttribute("data-ul"));

        // let text = ""

        if (actual){
            if (rda) {
                let white_width = total_width * (actual / rda);
                if (white_width >= total_width){
                    red_bar.style.backgroundColor = "#f55";
                }
                white_bar.style.width = white_width + "px";
            } 
            // else {
            //     text += " no rda"
            // }
        
            if (ul) {
                let red_width = total_width * (actual / ul);
                if (red_width >= total_width){
                    red_width = total_width;
                    red_bar.style.backgroundColor = "#b00";
                }
                red_bar.style.width = red_width + "px";
            } 
            // else {
            //     text += " no ul"
            // }
        
            // let textNode = document.createTextNode(text)
            // let textSpan = document.createElement("span")
            // textSpan.appendChild(textNode)
            // loading_bar.parentElement.append(textSpan)
        }
        if (!rda && !ul){
            loading_bar.style.backgroundColor = "#555"
            loading_bar.innerHTML = "&nbsp;no RDA and U</span>"
        }
    }
}

loading_bar_init()