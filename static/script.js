const scrollAmount = 400;

document.querySelectorAll(".scroll-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const targetClass = btn.dataset.target;
    const row = document.querySelector(`.movie-row.${targetClass}`);
    if (!row) return;

    if (btn.classList.contains("scroll-left")) {
      row.scrollBy({ left: -scrollAmount, behavior: "smooth" });
    } else {
      row.scrollBy({ left: scrollAmount, behavior: "smooth" });
    }
  });
});

// Mobile navbar toggle
const menuToggle = document.getElementById("menu-toggle");
const navLinks = document.querySelector(".nav-links");

if (menuToggle && navLinks) {
  menuToggle.addEventListener("click", () => {
    navLinks.classList.toggle("show");
  });
}

