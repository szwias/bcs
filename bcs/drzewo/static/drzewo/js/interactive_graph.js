const tooltip = d3.select("#tooltip");
const svg = d3.select("#svg");
const g = svg.append("g");
const linkLayer = g.append("g").attr("id", "links-layer");
const nodeLayer = g.append("g").attr("id", "nodes-layer");
const overlayLayer = g.append("g").attr("id", "overlay-layer"); // for year lines, guides, etc.

const zoom = d3
  .zoom()
  .scaleExtent([0.1, 10])
  .on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);

// Use Django-provided 'onp' value from the view
const onp = window.TREE_CONFIG.onp;
const dataUrl = `/drzewo/full-tree-data/?only_known_parents=${onp}`;

let nodesData = [],
  linksData = [],
  yearsData = {};
console.log("Fetching:", dataUrl);

fetch(dataUrl)
  .then((res) => res.json())
  .then((data) => {
    nodesData = data.nodes;
    linksData = data.links;
    yearsData = data.years;
    renderGraph();
  });

// Unified dark palette (matches your SCSS)
const palette = {
  background: "#1e1e1e",
  textMuted: "#d0d6e0",
  field: "#9fb4cc",
  accent: "#58a6ff",
  category: "#f5dd5d",
  border: "#888",
  toggle: "#999",
};

function renderGraph() {
  linkLayer.selectAll("*").remove();
  nodeLayer.selectAll("*").remove();
  svg.style("background-color", palette.background);

  const nodeById = new Map(nodesData.map((d) => [d.id, d]));

  // Links
  linkLayer
    .selectAll("line.link")
    .data(linksData)
    .enter()
    .append("line")
    .attr("class", "link")
    .attr("stroke", palette.border)
    .attr("stroke-width", 2)
    .attr("x1", (d) => nodeById.get(d.source).x_norm)
    .attr("y1", (d) => nodeById.get(d.source).y_norm)
    .attr("x2", (d) => nodeById.get(d.target).x_norm)
    .attr("y2", (d) => nodeById.get(d.target).y_norm);

  // Nodes
  const node = nodeLayer
    .selectAll("g.node")
    .data(nodesData)
    .enter()
    .append("g")
    .attr("class", "node")
    .attr("transform", (d) => `translate(${d.x_norm},${d.y_norm})`)
    .on("click", (_, d) => {
      if (d.url) window.open(d.url, "_blank");
    })
    .on("mouseover", (event, d) => {
      tooltip
        .style("display", "block")
        .style("background", "#2b2b2b")
        .style("color", palette.textMuted)
        .text(d.name);
      d3.select(event.currentTarget).classed("hover", true);
    })
    .on("mousemove", (event) => {
      const svgRect = svg.node().getBoundingClientRect();
      tooltip
        .style("left", event.clientX - svgRect.left + 10 + "px")
        .style("top", event.clientY - svgRect.top + 10 + "px");
    })
    .on("mouseout", (event) => {
      tooltip.style("display", "none");
      d3.select(event.currentTarget).classed("hover", false);
    });

  const node_radius = 25;

  node
    .append("circle")
    .attr("r", node_radius)
    .attr("fill", (d) => d.color || palette.accent)
    .attr("stroke", palette.border)
    .attr("stroke-width", 1.2);

  node
    .append("text")
    .attr("y", node_radius + 30)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .text((d) => d.name)
    .style("fill", palette.textMuted)
    .style("font-size", "15px")
    .style("pointer-events", "none");

  // Year lines
  Object.entries(yearsData).forEach(([year, reprNodeName]) => {
    const reprNode = nodesData.find((n) => n.name === reprNodeName);
    if (!reprNode) return; // safety
    const padding = 60
    const y = reprNode.y_norm - padding;
    // Draw horizontal line across the graph at this y
    g.append("line")
      .attr("x1", d3.min(nodesData, (d) => d.x_norm) - 100)
      .attr("x2", d3.max(nodesData, (d) => d.x_norm) + 100)
      .attr("y1", y)
      .attr("y2", y)
      .attr("stroke", "#555")
      .attr("stroke-dasharray", "4 2")
      .attr("stroke-width", 1.2);

    // Add year label on the left
    g.append("text")
      .attr("x", d3.min(nodesData, (d) => d.x_norm) - 150)
      .attr("y", y + 4)
      .attr("text-anchor", "end")
      .style("fill", palette.textMuted)
      .style("font-size", "70px")
      .text(year);
  });

  fitToView();
}

function fitToView() {
  if (!nodesData.length) return;
  const xs = nodesData.map((d) => d.x_norm);
  const ys = nodesData.map((d) => d.y_norm);
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
  svg.transition().duration(600).call(zoom.transform, transform);
}

// Sidebar color-mode (unchanged)
document.getElementById("color-mode").addEventListener("change", (e) => {
  const legend = d3.select("#legend");
  legend.selectAll("*").remove();

  const mode = e.target.value;
  if (mode === "none") nodesData.forEach((n) => (n.color = palette.accent));
  else if (mode === "generation") {
    const ys = [...new Set(nodesData.map((n) => Math.round(n.y_norm)))].sort(
      (a, b) => a - b
    );
    nodesData.forEach((n) => {
      const idx = ys.indexOf(n.y_norm);
      const hue = Math.round((360 * idx) / Math.max(1, ys.length - 1));
      n.color = `hsl(${hue} 70% 55%)`;
    });
    appendLegend(legend, "Jak sama nazwa wskazuje");
  } else if (mode === "status") {
    const statusMapping = {
      CZ: ["Członkowie zwyczajni", "#04ff00"],
      CW: ["Członkowie wspierający", "#ffea00"],
      X: ["Członkowie wydaleni", "rgba(255,255,255,0)"],
      W: ["Weterani", "#668daa"],
      H: ["Członkowie honorowi", "#ff9e01"],
    };
    applyMode(legend, statusMapping, mode);
  } else if (mode === "aktywnosc") {
    const aktywnoscMapping = {
      A: ["Członkowie aktywni", "#04ff00"],
      M: ["Członkowie mało aktywni", "#ffea00"],
      N: ["Członkowie nieaktywni", "#668daa"],
      O: ["Członkowie utraceni", "#ff0303"],
    };
    applyMode(legend, aktywnoscMapping, mode);
  }
  renderGraph();
});

function applyMode(legend, mapping, attribute) {
  Object.entries(mapping).forEach(([_, [desc, color]]) => {
    appendLegend(legend, desc, color);
  });

  nodesData.forEach((n) => {
    const key = n[attribute];
    const colorInfo = mapping[key];
    n.color = colorInfo ? colorInfo[1] : palette.toggle;
  });
}

function appendLegend(legend, entry = "", color = null) {
  const background_string = color ? `background: ${color};` : "";
  legend
    .append("div")
    .style("display", "flex")
    .style("align-items", "center")
    .style("margin-bottom", "4px").html(`
      <div style="width:20px;height:20px;${background_string} margin-right:6px;border:1px solid #222;"></div>
      ${entry}
    `);
}
