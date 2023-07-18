var deviSlide = document.getElementById('deviSlide'),
        deviSliderDiv = document.getElementById("deviSliderAmount"),
    gilesSlide = document.getElementById('gilesSlide'),
        gilesSliderDiv = document.getElementById("gilesSliderAmount");

deviSlide.oninput = function() {
    deviSliderDiv.innerHTML =  this.value + " talents";
}

gilesSlide.oninput = function() {
    gilesSliderDiv.innerHTML =  this.value + " talents";
}