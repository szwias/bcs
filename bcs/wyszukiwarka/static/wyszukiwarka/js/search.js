function toggleSection(header) {
  const appBlock = header.parentElement; // .search__app
  const indicator = header.querySelector(".search__app-indicator");

  appBlock.classList.toggle("search__app--open");

  if (indicator) {
    indicator.textContent = appBlock.classList.contains("search__app--open")
      ? "[-]"
      : "[+]";
  }
}
