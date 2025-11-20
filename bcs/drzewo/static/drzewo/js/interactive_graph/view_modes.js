import { palette } from "./colors.js";

export class ViewModes {
  constructor(state, nodeLayer, overlayLayer) {
    this.state = state;
    this.nodeLayer = nodeLayer;
    this.overlayLayer = overlayLayer;
    this.customColor = "#ff0000";
  }

  applyViewModes(activeViewModes) {
    // Reset all effects first
    this.nodeLayer
      .selectAll("circle")
      .style("fill", (d) => d.gradient || d.color || palette.accent)
      .style("opacity", 1);
    this.nodeLayer.selectAll("text").style("opacity", 1);
    this.overlayLayer.selectAll("*").remove();

    if (activeViewModes.has("years")) this.drawYearLines();
    if (activeViewModes.has("descendants")) {
      this.nodeLayer.selectAll("circle").style("opacity", this.state.lowerOpacity);
      this.nodeLayer.selectAll("text").style("opacity", this.state.lowerOpacity);
    }
    const colorPicker = d3.select("#color-picker");
    if (activeViewModes.has("color-nodes")) {
      colorPicker.style("display", "block");
      d3.select("#node-color-input").on("input", event => {
        this.customColor = event.target.value;
      });
    } else {
      colorPicker.style("display", "none");
    }
  }

  drawYearLines() {
    Object.entries(this.state.years).forEach(([year, reprNodeName]) => {
      const reprNode = this.state.nodes.find((n) => n.name === reprNodeName);
      if (!reprNode) return;
      const padding = this.state.layerDistance / 2;
      const y = reprNode.y_norm - padding;

      this.overlayLayer
        .append("line")
        .attr("x1", d3.min(this.state.nodes, (d) => d.x_norm) - 100)
        .attr("x2", d3.max(this.state.nodes, (d) => d.x_norm) + 100)
        .attr("y1", y)
        .attr("y2", y)
        .attr("stroke", "#555")
        .attr("stroke-dasharray", "4 2")
        .attr("stroke-width", 3);

      this.overlayLayer
        .append("text")
        .attr("x", d3.min(this.state.nodes, (d) => d.x_norm) - 150)
        .attr("y", y + 4)
        .attr("text-anchor", "end")
        .style("fill", palette.textMuted)
        .style("font-size", "70px")
        .text(year);
    });
  }
}
