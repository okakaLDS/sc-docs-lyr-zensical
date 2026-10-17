document$.subscribe(function () {
  document.querySelectorAll(".md-clipboard").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.classList.add("docs-copied");
      setTimeout(function () {
        btn.classList.remove("docs-copied");
      }, 600);
    });
  });
});
