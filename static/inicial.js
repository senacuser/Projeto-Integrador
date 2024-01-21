const dropBTN = document.querySelector(".drop-btn");
const nav = document.querySelector(".navbar");
const menu = document.querySelector(".menu");
const title = document.querySelectorAll(".main-title");

// Container da imagem e texto da página sobre
const img_container = document.querySelector('.img-container');
const inner_container = document.querySelector('.inner-container') ;

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

// Animação da imagem e texto da página sobre
window.addEventListener('load', () => {
  img_container.classList.add('img-container-active')
  inner_container.classList.add('inner-container-active')
})

// Slide dos textos usando a API IntersectionObserver
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

title.forEach((el) => {
  observer.observe(el);
});
