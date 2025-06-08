document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("toggle-sidebar");
  const sidebar = document.getElementById("sidebar");

  toggleBtn.addEventListener("click", function (e) {
    e.preventDefault();
    sidebar.classList.toggle("sidebar-collapsed");
  });
});