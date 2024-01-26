const dropBTN = document.querySelector(".drop-btn"),
      nav = document.querySelector(".navbar"),
      menu = document.querySelector(".menu"),
      title = document.querySelectorAll(".main-title"),
      solutionsSectionItems = document.querySelector('.our-solutions-section-items'),
      solutionsCards = document.querySelectorAll('.our-solutions-cards');


// Container da imagem e texto da página sobre
const img_container = document.querySelector('.img-container'),
      inner_container = document.querySelector('.inner-container');

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

// Animação dos cards da página sobre -- Trabalho em progresso

const newObserver = new IntersectionObserver((newEntries) => {
  newEntries.forEach((newEntry) => {
    if (newEntry.isIntersecting) {
      solutionsCards.forEach((cards) => {
        setInterval(() => {
          cards.style.visibility = 'visible';
          cards.style.transform = 'scale(1)';
        }, 500)
      })
    }
  })
})

title.forEach((el) => {
  observer.observe(el);
});

newObserver.observe(solutionsSectionItems);