import { palette } from "./colors.js";
import { ColorModes } from "./color_modes.js";
import { ViewModes } from "./view_modes.js";
import { getDescendants } from "./utils.js";

export class EventListener {
  constructor(
    state,
    svg,
    defs,
    nodeLayer,
    overlayLayer,
    tooltip,
    graph,
    activeViewModes
  ) {
    this.state = state;
    this.svg = svg;
    this.defs = defs;
    this.nodeLayer = nodeLayer;
    this.overlayLayer = overlayLayer;
    this.tooltip = tooltip;
    this.graph = graph;
    this.activeViewModes = activeViewModes;

    this.viewModes = new ViewModes(
      this.state,
      this.nodeLayer,
      this.overlayLayer
    );

    this.colorModes = new ColorModes(this.state);

    this.graph.setEventHandlers({
      mouseOver: this.handleMouseOver.bind(this),
      mouseMove: this.handleMouseMove.bind(this),
      mouseOut: this.handleMouseOut.bind(this),
      click: this.handleClick.bind(this),
    });
  }

  listen() {
    document.getElementById("color-mode").addEventListener("change", (e) => {
      this.colorModes.clearModes();
      const mode = e.target.value;
      this.colorModes.applyMode(mode);
      this.graph.renderGraph();
      this.viewModes.applyViewModes(this.activeViewModes);
    });

    document.querySelectorAll(".view-mode").forEach((checkbox) => {
      checkbox.addEventListener("change", (e) => {
        const mode = e.target.value;
        if (e.target.checked) this.activeViewModes.add(mode);
        else this.activeViewModes.delete(mode);
        this.viewModes.applyViewModes(this.activeViewModes);
      });
    });

    this.nodeLayer
      .selectAll("g.node")
      .on("mouseover", (event, d) => this.handleMouseOver(event, d))
      .on("mousemove", (event, d) => this.handleMouseMove(event, d))
      .on("mouseout", (event, d) => this.handleMouseOut(event, d))
      .on("click", (event, d) => this.handleClick(event, d));

    this.graph.renderGraph();
  }

  handleClick = (event, d) => {
    if (this.activeViewModes.has("color-nodes")) {
      d.color = this.viewModes.customColor;
      d3.select(event.currentTarget).select("circle").attr("fill", d.color);
      this.graph.renderGraph(false);
    } else {
      if (d.url) window.open(d.url, "_blank");
    }
  };

  handleMouseOver = (event, d) => {
    this.tooltip
      .style("display", "block")
      .style("background", palette.tooltipBg)
      .style("color", palette.textMuted)
      .text(d.name);
    d3.select(event.currentTarget).classed("hover", true);

    // Extra: descendants highlighting
    if (this.activeViewModes.has("descendants")) {
      const descendants = getDescendants(d.pk, this.state.childrenDict);
      descendants.add(d.pk); // include self

      this.nodeLayer.selectAll("g.node").each(function (n) {
        const highlight = descendants.has(n.pk);
        d3.select(this)
          .select("circle")
          .style("opacity", highlight ? 1 : ViewModes.lowerOpacity);
        d3.select(this)
          .select("text")
          .style("opacity", highlight ? 1 : ViewModes.lowerOpacity);
      });
    }
  };

  handleMouseMove = (event, d) => {
    const svgRect = this.svg.node().getBoundingClientRect();
    this.tooltip
      .style("left", event.clientX - svgRect.left + 10 + "px")
      .style("top", event.clientY - svgRect.top + 10 + "px");
  };

  handleMouseOut = (event, d) => {
    this.tooltip.style("display", "none");
    d3.select(event.currentTarget).classed("hover", false);

    // Restore normal opacity if descendants view-mode was active
    if (this.activeViewModes.has("descendants")) {
      this.nodeLayer
        .selectAll("circle")
        .style("opacity", ViewModes.lowerOpacity);
      this.nodeLayer.selectAll("text").style("opacity", ViewModes.lowerOpacity);
    }
  };
}
