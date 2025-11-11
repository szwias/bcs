import { Graph } from "./graph.js";
import { EventListener } from "./events.js";

// ====== State ======
const state = {
  nodes: [],
  links: [],
  years: {},
  helperDict: {},
  layerDistance: 0,
};

// ====== Layers ======
const tooltip = d3.select("#tooltip");
const svg = d3.select("#svg");
const g = svg.append("g");
const linkLayer = g.append("g").attr("id", "links-layer");
const nodeLayer = g.append("g").attr("id", "nodes-layer");
const overlayLayer = g.append("g").attr("id", "overlay-layer");

// ====== Zoom ======
const zoom = d3
  .zoom()
  .scaleExtent([0.1, 10])
  .on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);

// ====== Miscellanous ======
let activeViewModes = new Set();

// ====== Data Fetch ======
async function fetchTreeData() {
  const onp = window.TREE_CONFIG.onp;
  const dataUrl = `/drzewo/full-tree-data/?only_known_parents=${onp}`;
  const res = await fetch(dataUrl);
  const data = await res.json();
  state.nodes = data.nodes;
  state.links = data.links;
  state.years = data.years;
  state.helperDict = data.helper_dict;
  state.layerDistance = data.layer_distance;
}

function reapplyModes() {
  // Apply modes AFTER data has been rendered
  const colorMode = document.getElementById("color-mode")?.value;
  if (colorMode)
    document.getElementById("color-mode").dispatchEvent(new Event("change"));
  // Reapply all view modes that are currently checked
  document.querySelectorAll(".view-mode:checked").forEach((checkbox) => {
    checkbox.dispatchEvent(new Event("change"));
  });
}

// ====== Init ======
async function init() {
  await fetchTreeData();
  const graph = new Graph(state, zoom, nodeLayer, linkLayer, svg);
  graph.renderGraph();
  const eventListener = new EventListener(
    state,
    svg,
    nodeLayer,
    overlayLayer,
    tooltip,
    graph,
    activeViewModes
  );
  eventListener.listen();
  reapplyModes();
}

void init();
