// Mostrar/ocultar menú lateral
function toggleMenu() {
  const menu = document.getElementById("side-menu");
  menu.classList.toggle("show");
}

// Mostrar/ocultar barra de búsqueda
function toggleSearchBar() {
  const form = document.querySelector(".search-form");
  form.classList.toggle("expanded");
}

// Cerrar menú y barra si se hace clic fuera
window.addEventListener("click", function (e) {
  const menu = document.getElementById("side-menu");
  const menuIcon = document.querySelector(".menu-icon");
  const searchForm = document.querySelector(".search-form");
  const searchToggle = document.querySelector(".search-toggle");

  if (!menu.contains(e.target) && !menuIcon.contains(e.target)) {
    menu.classList.remove("show");
  }

  if (!searchForm.contains(e.target) && !searchToggle.contains(e.target)) {
    searchForm.classList.remove("expanded");
  }
});

// Carrusel general
function scrollCarousel(trackId, direction = 1) {
  const track = document.getElementById(trackId);
  const scrollAmount = track.clientWidth * 0.6;
  track.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}

// Scroll automático infinito
function autoScrollCarouselLoop(trackId, interval = 4000) {
  const track = document.getElementById(trackId);
  let paused = false;

  const loop = setInterval(() => {
    if (paused) return;

    const maxScroll = track.scrollWidth - track.clientWidth;
    const atEnd = Math.ceil(track.scrollLeft) >= maxScroll;

    if (atEnd) {
      track.scrollTo({ left: 0, behavior: 'smooth' });
    } else {
      scrollCarousel(trackId, 1);
    }
  }, interval);

  track.addEventListener('mouseover', () => paused = true);
  track.addEventListener('mouseout', () => paused = false);
}

// Cargar después de renderizado
window.addEventListener("DOMContentLoaded", () => {
  autoScrollCarouselLoop('carousel-track-books');
  autoScrollCarouselLoop('carousel-track-peliculas');
});

// Funciones individuales por sección
function scrollCarouselBooks(dir) {
  scrollCarousel('carousel-track-books', dir);
}

function scrollCarouselPeliculas(dir) {
  scrollCarousel('carousel-track-peliculas', dir);
}



function openModal() {
  document.getElementById("loginModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("loginModal").style.display = "none";
}


  // Cierra el modal si se hace clic fuera del contenido
 window.onclick = function(event) {
  const modal = document.getElementById("loginModal");
  if (event.target === modal) {
    modal.style.display = "none";
  }
}


// barra busqueda inicio
  
  document.getElementById("form-busqueda").addEventListener("submit", function (e) {
    e.preventDefault();

    const q = document.querySelector(".search-input").value.trim();
    const tipo = document.querySelector(".search-select").value;

    if (!q) return; // No hacer nada si el campo está vacío

    const ruta = tipo === "peliculas" ? "/peliculas" : "/libros";
    const query = encodeURIComponent(q);

    // Redirigir con parámetro GET
    window.location.href = `${ruta}?titulo=${query}`;
  });

 

