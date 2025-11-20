export function changeOpacity(nodeLayer, conditionFunc, opacity) {
  nodeLayer
    .selectAll("g.node circle")
    .style("opacity", (d) => (conditionFunc(d) ? opacity : 1));
  nodeLayer
    .selectAll("g.node text")
    .style("opacity", (d) => (conditionFunc(d) ? opacity : 1));
}

export function applyGradient(
  colorMap,
  nodeAttribute,
  fallbackProc,
  defs,
  state
) {
  colorMap.forEach((colors, nodeId) => {
    const gradId = `grad-${nodeId}`;
    defs.select(`#${gradId}`).remove();

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
  state.nodes.forEach((node) => {
    if (colorMap.has(node[nodeAttribute])) {
      node.gradient = `url(#grad-${node[nodeAttribute]})`;
    } else {
      fallbackProc(node);
    }
  });
}
