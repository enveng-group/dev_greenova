
const scrollCharts = function (id, direction) {
  const container = document.getElementById(id);
  const scrollAmount = 350;
  const scrollAmountDirection = (direction === 'left') ? (-scrollAmount) : scrollAmount;
  container.scrollBy({ left: scrollAmountDirection, behavior: 'smooth' });
};