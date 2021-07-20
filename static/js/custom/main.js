let toggle_btn = document.getElementById("nav-toggle");
let mobile_nav = document.getElementById("mobile-nav");

toggle_btn.addEventListener("click", () => {
    mobile_nav.classList.toggle("flex");
    mobile_nav.classList.toggle("hidden");
})