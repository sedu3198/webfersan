const carouselContainer = document.querySelector('.carousel-container');
const cards = Array.from(document.querySelectorAll('.agency-card'));
const leftBtn = document.querySelector('.left-btn');
const rightBtn = document.querySelector('.right-btn');
let currentIndex = 0;
let interval;
const offset = 0; // Sin desplazamiento inicial para resaltar la tarjeta correcta

// Calcula el desplazamiento para el carrusel
// Calcula el desplazamiento necesario para centrar la tarjeta activa
const calculateOffsetX = () => {
  const containerWidth = carouselContainer.offsetWidth;
  const cardWidth = cards[0].offsetWidth;
  const gap = 21; // Ancho del espacio entre tarjetas
  const totalCardWidth = cardWidth + gap;

  // Centra la tarjeta activa
  return -(currentIndex * totalCardWidth) + (containerWidth / 2 - cardWidth / 2);
};

// Actualiza el carrusel al cambiar la posición
function updateCarousel() {
  cards.forEach(card => card.classList.remove('active'));
  const activeIndex = (currentIndex + offset) % cards.length;
  cards[activeIndex].classList.add('active');

  const offsetX = calculateOffsetX();
  carouselContainer.style.transform = `translateX(${offsetX}px)`;
}

// Inicia el carrusel automático
function startCarousel() {
  if (interval) clearInterval(interval);
  interval = setInterval(() => {
    currentIndex = (currentIndex + 1) % cards.length;
    updateCarousel();
  }, 3000); // Cambia cada 3 segundos
}

// Detiene el carrusel automático
function stopCarousel() {
  clearInterval(interval);
  interval = null;
}

// Muestra el modal con información específica
function showInfo(agency) {
  stopCarousel();

  const modal = document.getElementById('info-modal');
  const modalText = document.getElementById('modal-text');
  const modalImage = document.getElementById('modal-image');

  const infoContent = {
    volkswagen: {
      image: "/static/images/jetta2024.png",
      text: "Volkswagen es una marca automovilística alemana fundada en 1937, conocida por modelos icónicos como el Golf y el Beetle."
    },
    suzuki: {
      image: "/static/images/swift2024.png",
      text: "Suzuki es una marca japonesa famosa por sus motocicletas, coches compactos y vehículos todoterreno."
    },
    harley: {
      image: "/static/images/harley2024.png",
      text: "Harley Davidson es una icónica marca estadounidense de motocicletas de gran cilindrada."
    },
    seat: {
      image: "/static/images/ibiza2024.png",
      text: "SEAT es una marca española de automóviles conocida por su diseño y tecnología avanzados."
    },
    omoda: {
      image: "/static/images/omoda2024.png",
      text: "Omoda es una marca innovadora en vehículos eléctricos, conocida por su enfoque en diseño y sostenibilidad."
    },
    sev: {
      image: "/static/images/sev2024.png",
      text: "SEV es una marca emergente que se enfoca en la movilidad eléctrica para el futuro."
    },
    zeekr: {
      image: "/static/images/zeekr2024.png",
      text: "Zeekr es conocida por sus vehículos eléctricos de alta gama y tecnología avanzada."
    },
    chirey: {
      image: "/static/images/chirey2024.png",
      text: "Chirey se enfoca en ofrecer vehículos confiables y accesibles, con énfasis en tecnología."
    },
    motornation: {
      image: "/static/images/motornation2024.png",
      text: "MotorNation es una empresa con enfoque en soluciones de movilidad globales y modernas."
    }
  };

  const content = infoContent[agency] || { image: '', text: 'No hay información disponible.' };

  modalImage.src = content.image;
  modalText.innerHTML = content.text;
  modal.style.display = 'flex';
}

// Cierra el modal y reanuda el carrusel
function closeInfo() {
  const modal = document.getElementById('info-modal');
  modal.style.display = 'none';
  startCarousel();
}

// Controla los botones de navegación
leftBtn.addEventListener('click', () => {
  currentIndex = currentIndex > 0 ? currentIndex - 1 : cards.length - 1;
  updateCarousel();
  pauseCarouselForButtons();
});

rightBtn.addEventListener('click', () => {
  currentIndex = (currentIndex + 1) % cards.length;
  updateCarousel();
  pauseCarouselForButtons();
});

// Pausa el carrusel unos segundos tras usar los botones
function pauseCarouselForButtons() {
  stopCarousel();
  setTimeout(startCarousel, 1000); // Pausa breve de 1 segundo
}

// Eventos de hover para detener y reanudar el carrusel
cards.forEach(card => {
  card.addEventListener('mouseenter', stopCarousel);
  card.addEventListener('mouseleave', startCarousel);
});

// Swipe para dispositivos táctiles
let startX = 0;

carouselContainer.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
});

carouselContainer.addEventListener('touchend', (e) => {
  const endX = e.changedTouches[0].clientX;
  const delta = endX - startX;

  if (delta > 50) {
    // Swipe a la derecha
    currentIndex = currentIndex > 0 ? currentIndex - 1 : cards.length - 1;
  } else if (delta < -50) {
    // Swipe a la izquierda
    currentIndex = (currentIndex + 1) % cards.length;
  }
  updateCarousel();
  pauseCarouselForButtons();
});

// Cierra el modal con el botón
document.querySelector('.close-btn').addEventListener('click', closeInfo);

// Inicia el carrusel
startCarousel();
updateCarousel(); // Actualiza el carrusel inmediatamente al cargar la página