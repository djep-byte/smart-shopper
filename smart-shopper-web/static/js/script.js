document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("compute-btn").onclick = computeRoute;
  document.getElementById("reset-btn").onclick = resetForm;
});

async function computeRoute() {
  const selected = Array.from(
    document.querySelectorAll('input[type="checkbox"]:checked')
  ).map((cb) => cb.value);
  if (selected.length === 0) {
    alert("Pilih minimal satu kategori!");
    return;
  }

  const resultEl = document.getElementById("result");
  const stepsEl = document.getElementById("steps");
  const distanceEl = document.getElementById("distance");

  resultEl.style.display = "block";
  stepsEl.innerHTML = "<li>Menghitung rute...</li>";
  distanceEl.textContent = "Menghitung...";

  try {
    const res = await fetch("/compute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ categories: selected }),
    });
    const data = await res.json();

    distanceEl.textContent = `${data.distance}`;
    stepsEl.innerHTML = "";
    if (!data.steps || data.steps.length === 0) {
      stepsEl.innerHTML = "<li>Tidak ditemukan rute.</li>";
    } else {
      data.steps.forEach((step) => {
        const li = document.createElement("li");
        li.textContent = step;
        stepsEl.appendChild(li);
      });
    }
    // scroll ke hasil
    resultEl.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    console.error(err);
    alert("Terjadi kesalahan saat menghitung rute.");
  }
}

function resetForm() {
  document
    .querySelectorAll('input[type="checkbox"]')
    .forEach((cb) => (cb.checked = false));
  document.getElementById("result").style.display = "none";
  document.getElementById("steps").innerHTML = "";
  document.getElementById("distance").textContent = "0";
}
