// ====== Palette from SCSS ======
export const palette = {
  background: getCssColor("--js-color-bg"),
  panel: getCssColor("--js-color-panel"),
  border: getCssColor("--js-color-border"),
  textMuted: getCssColor("--js-color-text"),
  accent: getCssColor("--js-color-accent"),
  field: getCssColor("--js-color-field"),
  toggle: getCssColor("--js-color-toggle"),
  tooltipBg: getCssColor("--js-color-tooltip-bg"),
  link: getCssColor("--js-color-link"),
};

function getCssColor(varName) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(varName)
    .trim();
}