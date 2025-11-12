import { palette } from "./colors.js";

export class Graph {
  constructor(state, zoom, nodeLayer, linkLayer, svg) {
    this.state = state;
    this.zoom = zoom;
    this.nodeLayer = nodeLayer;
    this.linkLayer = linkLayer;
    this.svg = svg;

    // callback storage
    this.onMouseOver = null;
    this.onMouseMove = null;
    this.onMouseOut = null;
    this.onClick = null;

    this.nodeRadius = 30;
    this.nodeById = new Map(this.state.nodes.map((d) => [d.id, d]));
  }

  setEventHandlers({ mouseOver, mouseMove, mouseOut, click }) {
    this.onMouseOver = mouseOver;
    this.onMouseMove = mouseMove;
    this.onMouseOut = mouseOut;
    this.onClick = click;
  }

  renderGraph(fitToView = true) {
    this.clearGraph();
    this.drawLinks();
    this.drawNodes();
    if (fitToView) this.fitToView();
  }

  clearGraph() {
    this.linkLayer.selectAll("*").remove();
    this.nodeLayer.selectAll("*").remove();
    this.svg.style("background-color", palette.background);
  }

  drawLinks() {
    this.linkLayer
      .selectAll("line.link")
      .data(this.state.links)
      .enter()
      .append("line")
      .attr("class", "link")
      .attr("stroke", palette.border)
      .attr("stroke-width", 3)
      .attr("stroke-dasharray", (d) => (d.type === "dashed" ? "30,30" : null))
      .attr("x1", (d) => this.nodeById.get(d.source).x_norm)
      .attr("y1", (d) => this.nodeById.get(d.source).y_norm)
      .attr("x2", (d) => this.nodeById.get(d.target).x_norm)
      .attr("y2", (d) => this.nodeById.get(d.target).y_norm);
  }

  drawNodes() {
    const node = this.nodeLayer
      .selectAll("g.node")
      .data(this.state.nodes)
      .enter()
      .append("g")
      .attr("class", "node")
      .attr("transform", (d) => `translate(${d.x_norm},${d.y_norm})`);

    // attach event handlers if they exist
    if (this.onMouseOver) node.on("mouseover", this.onMouseOver);
    if (this.onMouseMove) node.on("mousemove", this.onMouseMove);
    if (this.onMouseOut) node.on("mouseout", this.onMouseOut);
    if (this.onClick) node.on("click", this.onClick);

    node
      .append("circle")
      .attr("r", this.nodeRadius)
      .attr("fill", (d) => d.color || palette.accent)
      .attr("stroke", palette.border)
      .attr("stroke-width", 1.2);

    node
      .append("text")
      .attr("y", this.nodeRadius + 30)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .text((d) => d.name)
      .style("fill", palette.textMuted)
      .style("font-size", "15px")
      .style("pointer-events", "none");
  }

  fitToView() {
    if (!this.state.nodes.length) return;
    const xs = this.state.nodes.map((d) => d.x_norm);
    const ys = this.state.nodes.map((d) => d.y_norm);
    const minX = Math.min(...xs),
      maxX = Math.max(...xs);
    const minY = Math.min(...ys),
      maxY = Math.max(...ys);
    const pad = 300;
    const contentW = maxX - minX + pad * 2;
    const contentH = maxY - minY + pad * 2;
    const svgW = document.getElementById("stage").clientWidth;
    const svgH = document.getElementById("stage").clientHeight;
    const scale = Math.min(svgW / contentW, svgH / contentH);
    const tx = -minX + pad;
    const ty = -minY + pad;

    const transform = d3.zoomIdentity
      .translate((svgW - contentW * scale) / 2, (svgH - contentH * scale) / 2)
      .scale(scale)
      .translate(tx, ty);

    this.svg.transition().duration(600).call(this.zoom.transform, transform);
  }
}
