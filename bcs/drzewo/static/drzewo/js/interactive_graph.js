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
  const nodeById = new Map(nodesData.map((d) => [d.id, d]));

  // Links
  g.selectAll("line.link")
    .data(linksData)
    .enter()
    .append("line")
    .attr("class", "link")
    .attr("stroke", "#666")
    .attr("stroke-width", 1)
    .attr("x1", (d) => nodeById.get(d.source).x_norm)
    .attr("y1", (d) => nodeById.get(d.source).y_norm)
    .attr("x2", (d) => nodeById.get(d.target).x_norm)
    .attr("y2", (d) => nodeById.get(d.target).y_norm);

  // Nodes
  const node = g
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
      tooltip.style("display", "block").text(d.name);
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
  // Elliptical node with centered label
  node
    .append("circle")
    .attr("x", (d) => -d.width / 2)
    .attr("y", (d) => -d.height / 2)
    .attr("r", node_radius)
    .attr("fill", (d) => d.color || "#66aaff")
    .attr("stroke", "#222")
    .attr("stroke-width", 1.2);

  node
    .append("text")
    .attr("y", node_radius + 30)
    .attr("text-anchor", "middle")
    .attr("dominant-baseline", "middle")
    .text((d) => d.name)
    .style("font-size", "15px")
    .style("pointer-events", "none");
}