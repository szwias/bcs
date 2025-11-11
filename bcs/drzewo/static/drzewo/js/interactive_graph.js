// ====== State ======
const state = {
  nodes: [],
  links: [],
  years: {},
  layerDistance: 0,
};

// ====== Layers ======
const tooltip = d3.select("#tooltip");
const svg = d3.select("#svg");
const g = svg.append("g");
const linkLayer = g.append("g").attr("id", "links-layer");
const nodeLayer = g.append("g").attr("id", "nodes-layer");
const overlayLayer = g.append("g").attr("id", "overlay-layer"); // year lines, guides

// ====== Palette from SCSS ======
const palette = {
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

// ====== Zoom ======
const zoom = d3
  .zoom()
  .scaleExtent([0.1, 10])
  .on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);

// ====== Data Fetch ======
function fetchTreeData() {
  const onp = window.TREE_CONFIG.onp;
  const dataUrl = `/drzewo/full-tree-data/?only_known_parents=${onp}`;
  fetch(dataUrl)
    .then((res) => res.json())
    .then((data) => {
      state.nodes = data.nodes;
      state.links = data.links;
      state.years = data.years;
      state.layerDistance = data.layer_distance;

      renderGraph();

      // Apply modes AFTER data has been rendered
        const colorMode = document.getElementById("color-mode")?.value;
        const viewMode = document.getElementById("view-mode")?.value;
        console.log("Applying saved modes:", colorMode, viewMode);
        if (colorMode)
          document.getElementById("color-mode").dispatchEvent(new Event("change"));
        if (viewMode)
          document.getElementById("view-mode").dispatchEvent(new Event("change"));
        });
}

// ====== Graph Rendering ======
function renderGraph() {
  clearGraph();
  const nodeById = new Map(state.nodes.map((d) => [d.id, d]));
  drawLinks(nodeById);
  drawNodes();
  fitToView();
}

function clearGraph() {
  linkLayer.selectAll("*").remove();
  nodeLayer.selectAll("*").remove();
  svg.style("background-color", palette.bg);
}

function drawLinks(nodeById) {
  linkLayer
    .selectAll("line.link")
    .data(state.links)
    .enter()
    .append("line")
    .attr("class", "link")
    .attr("stroke", palette.border)
    .attr("stroke-width", 2)
    .attr("x1", (d) => nodeById.get(d.source).x_norm)
    .attr("y1", (d) => nodeById.get(d.source).y_norm)
    .attr("x2", (d) => nodeById.get(d.target).x_norm)
    .attr("y2", (d) => nodeById.get(d.target).y_norm);
}

function drawNodes() {
  const node = nodeLayer
    .selectAll("g.node")
    .data(state.nodes)
    .enter()
    .append("g")
    .attr("class", "node")
    .attr("transform", (d) => `translate(${d.x_norm},${d.y_norm})`)
    .on("click", (_, d) => {
      if (d.url) window.open(d.url, "_blank");
    })
    .on("mouseover", handleMouseOver)
    .on("mousemove", handleMouseMove)
    .on("mouseout", handleMouseOut);

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
    .style("fill", palette.text)
    .style("font-size", "15px")
    .style("pointer-events", "none");
}

// ====== Tooltip Handlers ======
function handleMouseOver(event, d) {
  tooltip
    .style("display", "block")
    .style("background", palette["tooltip-bg"])
    .style("color", palette.text)
    .text(d.name);
  d3.select(event.currentTarget).classed("hover", true);
}

function handleMouseMove(event) {
  const svgRect = svg.node().getBoundingClientRect();
  tooltip
    .style("left", event.clientX - svgRect.left + 10 + "px")
    .style("top", event.clientY - svgRect.top + 10 + "px");
}

function handleMouseOut(event) {
  tooltip.style("display", "none");
  d3.select(event.currentTarget).classed("hover", false);
}

// ====== Fit to View ======
function fitToView() {
  if (!state.nodes.length) return;
  const xs = state.nodes.map((d) => d.x_norm);
  const ys = state.nodes.map((d) => d.y_norm);
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

// ====== Color Modes ======
function applyMode(legend, mapping, attribute) {
  Object.entries(mapping).forEach(([_, [desc, color]]) =>
    appendLegend(legend, desc, color)
  );
  state.nodes.forEach((n) => {
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
    .style("margin-bottom", "4px")
    .html(
      `<div style="width:20px;height:20px;${background_string} margin-right:6px;border:1px solid #222;"></div>${entry}`
    );
}

// ====== View Modes ======
function drawYearLines() {
  overlayLayer.selectAll("*").remove();
  Object.entries(state.years).forEach(([year, reprNodeName]) => {
    const reprNode = state.nodes.find((n) => n.name === reprNodeName);
    if (!reprNode) return;
    const padding = state.layerDistance / 2;
    const y = reprNode.y_norm - padding;

    overlayLayer
      .append("line")
      .attr("x1", d3.min(state.nodes, (d) => d.x_norm) - 100)
      .attr("x2", d3.max(state.nodes, (d) => d.x_norm) + 100)
      .attr("y1", y)
      .attr("y2", y)
      .attr("stroke", "#555")
      .attr("stroke-dasharray", "4 2")
      .attr("stroke-width", 3);

    overlayLayer
      .append("text")
      .attr("x", d3.min(state.nodes, (d) => d.x_norm) - 150)
      .attr("y", y + 4)
      .attr("text-anchor", "end")
      .style("fill", palette.textMuted)
      .style("font-size", "70px")
      .text(year);
  });
}

// ====== Event Listeners ======
function initEventListeners() {
  document.getElementById("color-mode").addEventListener("change", (e) => {
    const legend = d3.select("#legend");
    legend.selectAll("*").remove();
    const mode = e.target.value;

    if (mode === "none") state.nodes.forEach((n) => (n.color = palette.accent));
    else if (mode === "generation") {
      const ys = [
        ...new Set(state.nodes.map((n) => Math.round(n.y_norm))),
      ].sort((a, b) => a - b);
      state.nodes.forEach((n) => {
        const idx = ys.indexOf(n.y_norm);
        const hue = Math.round((360 * idx) / Math.max(1, ys.length - 1));
        n.color = `hsl(${hue} 70% 55%)`;
      });
      appendLegend(legend, "Jak sama nazwa wskazuje");
    } else if (mode === "status") {
      applyMode(
        legend,
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
      applyMode(
        legend,
        {
          A: ["Członkowie aktywni", "#04ff00"],
          M: ["Członkowie mało aktywni", "#ffea00"],
          N: ["Członkowie nieaktywni", "#668daa"],
          O: ["Członkowie utraceni", "#ff0303"],
        },
        "aktywnosc"
      );
    }

    renderGraph();
  });

  document.getElementById("view-mode").addEventListener("change", (e) => {
    const mode = e.target.value;
    overlayLayer.selectAll("*").remove();
    if (mode === "years") drawYearLines();
  });
}

// ====== Init ======
function init() {
  fetchTreeData();
  initEventListeners();
}

init();
