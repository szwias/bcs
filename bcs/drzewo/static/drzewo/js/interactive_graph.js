const svg = d3.select("#svg");
const g = svg.append("g");
const tooltip = d3.select("#tooltip");

const zoom = d3
  .zoom()
  .scaleExtent([0.1, 10])
  .on("zoom", (event) => g.attr("transform", event.transform));
svg.call(zoom);

// Use Django-provided 'onp' value from the view
const onp = window.TREE_CONFIG.onp;
const dataUrl = `/drzewo/full-tree-data/?only_known_parents=${onp}`;

let nodesData = [],
  linksData = [];
console.log("Fetching:", dataUrl);

fetch(dataUrl)
  .then((res) => res.json())
  .then((data) => {
    nodesData = data.nodes;
    linksData = data.links;
    renderGraph();
  });

function renderGraph() {
    g.selectAll("*").remove();
}