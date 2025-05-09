// modal.js
function openModal(imageUrl) {
  document.getElementById('modalImage').src = imageUrl;
  document.getElementById('imageModal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('imageModal').classList.add('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('imageModal');
  if (modal) {
    modal.addEventListener('click', function (e) {
      if (e.target.id === 'imageModal') {
        closeModal();
      }
    });
  }
});

// Optional: Filter states
function filterStates(query) {
  const items = document.querySelectorAll('#state-list li');
  items.forEach(item => {
    const match = item.textContent.toLowerCase().includes(query.toLowerCase());
    item.style.display = match ? 'block' : 'none';
  });
}
