document.addEventListener('DOMContentLoaded', async () => {
  // Fetch products from API
  const response = await fetch('http://localhost:5000/api/products');
  const products = await response.json();

  const track = document.querySelector('.carousel-track');
  const prev = document.querySelector('.carousel-button.prev');
  const next = document.querySelector('.carousel-button.next');

  // Create carousel items
  products.forEach(product => {
    const item = document.createElement('div');
    item.className = 'carousel-item';
    item.innerHTML = `
      <img src="${product.imageUrl}" alt="${product.productDisplayName}" style="width: 100%; height: 200px; object-fit: cover;">
      <div style="padding: 1rem;">
        <h3>${product.productDisplayName}</h3>
        <p>${product.price}</p>
      </div>
    `;
    track.appendChild(item);
  });

  let currentIndex = 0;

  function updateCarousel() {
    const itemWidth = 300 + 32; // width + margin
    track.style.transform = `translateX(-${currentIndex * itemWidth}px)`;
  }

  prev.addEventListener('click', () => {
    currentIndex = Math.max(currentIndex - 1, 0);
    updateCarousel();
  });

  next.addEventListener('click', () => {
    const maxIndex = track.children.length - Math.floor(track.parentElement.offsetWidth / (300 + 32));
    currentIndex = Math.min(currentIndex + 1, maxIndex);
    updateCarousel();
  });
});