function toggleCategory(header) {
  const list = header.nextElementSibling;
  if (!list) return;

  if (list.style.display === "none" || list.style.display === "") {
    list.style.display = "block";
  } else {
    list.style.display = "none";
  }
}
