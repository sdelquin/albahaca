document.addEventListener("DOMContentLoaded", function () {
  new Glide(".glide", {
    type: "carousel",
    perView: 4,
    gap: 24,
    swipeThreshold: 40,
    dragThreshold: 80,
    animationDuration: 400,
    breakpoints: {
      768: {
        perView: 1,
      },
    },
  }).mount();
});
