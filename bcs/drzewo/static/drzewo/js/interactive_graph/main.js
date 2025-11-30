import { Graph } from "./graph.js";
import { EventListener } from "./events.js";

// ====== State ======
const state = {
  nodes: [],
  nodesByName: {},
  nodesByPK: {},
  nodesByYear: {},
  links: [],
  years: {},
  childrenDict: {},
  layerDistance: 0,
  currentYear: 0,
  lowerOpacity: 0,
};

// ====== Layers ======
const tooltip = d3.select("#tooltip");
const svg = d3.select("#svg");
const defs = svg.append("defs");
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

// ====== Miscellaneous ======
const activeViewModes = new Set();

// ====== Data Fetch ======
async function fetchTreeData() {
  const onp = window.TREE_CONFIG.onp;
  const beans = window.TREE_CONFIG.beans;
  const dataUrl = `/drzewo/full-tree-data/?only_known_parents=${onp}&beans_present=${beans}`;
  const res = await fetch(dataUrl);
  const data = await res.json();
  state.nodes = data.nodes;
  state.nodesByName = new Map(state.nodes.map((n) => [n.name, n]));
  state.nodesByPK = new Map(state.nodes.map((n) => [n.pk, n]));
  state.nodesByYear = state.nodes.reduce((map, node) => {
    if (!map.has(node.year)) map.set(node.year, []);
    map.get(node.year).push(node);
    return map;
  }, new Map());
  state.nodesByYear = new Map(state.nodes.map((n) => [n.year, n]));
  state.links = data.links;
  state.years = data.years;
  state.childrenDict = data.childrenDict;
  state.layerDistance = data.layerDistance;
  state.currentYear = data.currentYear;
  state.lowerOpacity = 0.2;
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
    defs,
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
