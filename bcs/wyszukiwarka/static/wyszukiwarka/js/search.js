function toggleSection(header) {
  const resultsDiv = header.nextElementSibling;
  if (resultsDiv.style.display === "none") {
    resultsDiv.style.display = "block";
    header.querySelector(".toggle-indicator").textContent = "[-]";
  } else {
    resultsDiv.style.display = "none";
    header.querySelector(".toggle-indicator").textContent = "[+]";
  }
}
