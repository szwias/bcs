import { palette } from "./colors.js";

export class ColorModes {
  constructor(state, legend) {
    this.state = state;
    this.legend = legend;
  }

  applyMode(mode) {
    if (mode === "none")
      this.state.nodes.forEach((n) => (n.color = palette.accent));
    else if (mode === "generation") {
      const ys = [
        ...new Set(this.state.nodes.map((n) => Math.round(n.y_norm))),
      ].sort((a, b) => a - b);
      this.state.nodes.forEach((n) => {
        const idx = ys.indexOf(n.y_norm);
        const hue = Math.round((360 * idx) / Math.max(1, ys.length - 1));
        n.color = `hsl(${hue} 70% 55%)`;
      });
      this.appendLegend("Jak sama nazwa wskazuje");
    } else if (mode === "status") {
      this.createLegend(
        {
          CZ: ["Członkowie zwyczajni", "#04ff00"],
          CW: ["Członkowie wspierający", "#ffea00"],
          X: ["Członkowie wydaleni", "rgb(255,3,3)"],
          W: ["Weterani", "#668daa"],
          H: ["Członkowie honorowi", "#ff9e01"],
        },
        "status"
      );
    } else if (mode === "aktywnosc") {
      this.createLegend(
        {
          A: ["Członkowie aktywni", "#04ff00"],
          M: ["Członkowie mało aktywni", "#ffea00"],
          N: ["Członkowie nieaktywni", "#668daa"],
          O: ["Członkowie utraceni", "#ff0303"],
        },
        "aktywnosc"
      );
    }
  }

  createLegend(mapping, attribute) {
    Object.entries(mapping).forEach(([_, [desc, color]]) =>
      this.appendLegend(desc, color)
    );
    this.state.nodes.forEach((n) => {
      const key = n[attribute];
      const colorInfo = mapping[key];
      n.color = colorInfo ? colorInfo[1] : palette.toggle;
    });
  }

  appendLegend(entry = "", color = null) {
    const background_string = color ? `background: ${color};` : "";
    this.legend
      .append("div")
      .style("display", "flex")
      .style("align-items", "center")
      .style("margin-bottom", "4px")
      .html(
        `<div style="width:20px;height:20px;${background_string} margin-right:6px;border:1px solid #222;"></div>${entry}`
      );
  }
}
