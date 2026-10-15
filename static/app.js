document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm || "Are you sure?")) event.preventDefault();
  });
});

function updateOrderTotals() {
  const form = document.getElementById("order-form");
  if (!form) return;
  let total = 0;
  form.querySelectorAll("tbody tr[data-price]").forEach((row) => {
    const price = Number(row.dataset.price || 0);
    const input = row.querySelector(".qty-input");
    let qty = Number(input.value || 0);
    const stock = Number(input.dataset.stock || 0);
    if (qty < 0) qty = 0;
    if (qty > stock) qty = stock;
    const line = price * qty;
    total += line;
    const output = row.querySelector(".line-total");
    if (output) output.textContent = "₹" + line.toFixed(2);
  });
  const output = document.getElementById("order-total");
  if (output) output.textContent = "₹" + total.toFixed(2);
}
document.querySelectorAll(".qty-input").forEach((input) => input.addEventListener("input", updateOrderTotals));
updateOrderTotals();
