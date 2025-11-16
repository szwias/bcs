import { palette } from "./colors.js";

export class ColorModes {
  constructor(state) {
    this.state = state;
    this.legend = d3.select("#legend");
    this.divs_changed = new Set();
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
    } else if (mode === "lineages") {
      const lineages_options = d3.select("#lineages-options");
      this.divs_changed.add("#lineages-options")
      if (lineages_options.select("input[type=checkbox").empty()) {
        lineages_options
            .html(
                `<br>
                <label>
                    <input type="checkbox" class="view-mode" value="active-predecessors">
                    Aktywni założyciele rodów
                </label>`
            )
      }
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

  appendLegend(entry = null, color = null) {
    const container = this.legend
      .append("div")
      .style("display", "flex")
      .style("align-items", "center")
      .style("margin-bottom", "4px");

    // Append the color box only if a color is provided
    if (color) {
        container
          .append("div")
          .style("width", "20px")
          .style("height", "20px")
          .style("background", color)
          .style("margin-right", "6px")
          .style("border", "1px solid #222");
    }

    if (entry) container.append("span").text(entry);

    this.divs_changed.add("#legend");
  }



  clearModes() {
    this.divs_changed.forEach(d => {
      let div = d3.select(d);
      div.selectAll("*").remove();
    })
  }
}
