import { palette } from "./colors.js";
import { getDescendants, getPredecessors } from "./utils.js";

export class ColorModes {
  constructor(state, svg, defs, graph) {
    this.state = state;
    this.svg = svg;
    this.defs = defs;
    this.graph = graph;

    this.options = {};
    this.divs_changed = new Set();
  }

  applyMode(mode) {
    this.clearModes();
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
      this.divs_changed.add("#color-mode-options");
      const options = [
        {
          id: "active-predecessors",
          text: "Aktywni założyciele rodów",
        }
      ];
      this.renderColorModeOptions(mode, options);

      const predecessors = getPredecessors(
        this.state,
        this.options[mode]["active-predecessors"],
        5
      );
      const pred_colors = new Map();
      predecessors.forEach((p, i) => {
        pred_colors.set(p, [(360 * i) / Math.max(1, predecessors.length)]);
      });
      const desc_colors = new Map();
      for (const p of predecessors) {
        const color = pred_colors.get(p)[0];
        const descendants = getDescendants(p.pk, this.state.childrenDict);
        for (const d of descendants) {
          if (!desc_colors.has(d)) {
            desc_colors.set(d, []);
          }
          desc_colors.get(d).push(color);
        }
      }
      const transformedPredColors = Array.from(pred_colors, ([node, color]) => [
        node.pk,
        color,
      ]);
      const allColors = new Map([...transformedPredColors, ...desc_colors]);
      this.applyGradient(
          allColors,
          "pk",
          (node) => {node.color = "#000000"},
          this.defs
      );
    }
    this.graph.renderGraph();
  }

  applyGradient(colorMap, nodeAttribute, fallbackProc, defs) {
    colorMap.forEach((colors, nodeId) => {
      const gradId = `grad-${nodeId}`;
      this.defs.select(`#${gradId}`).remove();

      const gradient = defs
          .append("linearGradient")
          .attr("id", gradId)
          .attr("x1", "0%")
          .attr("y1", "0%")
          .attr("x2", "100%")
          .attr("y2", "0%");

      colors.forEach((color, i) => {
        const start = (i / colors.length) * 100;
        const end = ((i + 1) / colors.length) * 100;

        gradient
            .append("stop")
            .attr("offset", `${start}%`)
            .attr("stop-color", `hsl(${color}, 70%, 55%)`);

        gradient
            .append("stop")
            .attr("offset", `${end}%`)
            .attr("stop-color", `hsl(${color}, 70%, 55%)`);
      });
    });

    // Assign to node
    this.state.nodes.forEach((node) => {
      if (colorMap.has(node[nodeAttribute])) {
        node.gradient = `url(#grad-${node[nodeAttribute]})`;
      } else {
        fallbackProc(node);
      }
    });
  }

  renderColorModeOptions(mode, options) {
    const container = document.getElementById("color-mode-options");
    container.innerHTML = "";
    const template = document.getElementById(
      "color-mode-options-checkbox-template"
    );

    const modeOptions = this.options[mode] || {};
    this.options[mode] = modeOptions;
    options.forEach((option) => {
      const node = template.content.cloneNode(true);
      const input = node.querySelector("input");
      input.id = option.id;
      input.checked = modeOptions[option.id] || false;
      node.querySelector(".checkbox-text").textContent = option.text;

      input.addEventListener("change", () => {
        modeOptions[option.id] = input.checked;
        this.applyMode(mode);
      });

      container.appendChild(node);
    });
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
    const template = document.getElementById("legend-item-template");
    const item = template.content.firstElementChild.cloneNode(true);
    item.style.display = "flex";
    if (color) {
      item.querySelector(".sidebar__legend-item-color").style.background =
        color;
    }
    if (entry) {
      item.querySelector(".sidebar__legend-item-text").textContent = entry;
    }
    document.getElementById("legend").appendChild(item);
    this.divs_changed.add("#legend");
  }

  clearModes() {
    this.divs_changed.forEach((d) => {
      let div = d3.select(d);
      div.selectAll("*").remove();
    });
    this.state.nodes.forEach((node) => {
      node.gradient = "";
      node.color = palette.accent;
    });
    this.graph.renderGraph();
  }
}
