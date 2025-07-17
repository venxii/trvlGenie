document.addEventListener("DOMContentLoaded", function () {
    const travelDaysSlider = document.getElementById("TravelDays");
    const daysValue = document.getElementById("daysValue");

    travelDaysSlider.addEventListener("input", function () {
        daysValue.textContent = travelDaysSlider.value;
    });
});