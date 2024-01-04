let dropBTN = document.querySelector(".drop-btn");
let nav = document.querySelector(".navbar");
let menu = document.querySelector(".menu");

// Classes para o menu-dropdown
dropBTN.addEventListener("click", () => {
  dropBTN.classList.toggle("btn-active");
  menu.classList.toggle("active");
  nav.classList.toggle("nav-active");
});

// Remove a ativação da `transition` quando a tela é redimensionada
window.addEventListener("resize", () => {
  nav.style.transition = "none";
  setTimeout(() => {
    nav.style.transition = "opacity 1s ease";
  }, 100);
});

// Slide dos textos
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("main-active");
      // observer.unobserve(entry.target)
    } else {
      entry.target.classList.remove("main-active");
    }
  });
});

let title = document.querySelectorAll(".main-title");
title.forEach((el) => {
  observer.observe(el);
});
