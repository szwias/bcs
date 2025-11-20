export function getPredecessors(state, ACTIVE_PREDECESSORS, YEARS_BACK) {
  const years = Object.keys(state.years).map((y) => parseInt(y, 10));
  const currentYear = Math.max(...years);

  const toVisit = state.nodes.filter(
    (node) =>
      node.year &&
      parseInt(node.year, 10) > currentYear - YEARS_BACK &&
      ["A", "M"].includes(node.aktywnosc)
  );
  const predecessors = [];
  const visited = new Set();

  while (toVisit.length > 0) {
    const node = toVisit.pop();
    if (visited.has(node)) continue;
    visited.add(node);
    if (node.aktywnosc === "N") {
      predecessors.push(node);
    } else {
      const parents = [];
      if (node.parent1 !== "Nie dotyczy" && state.nodesByName.has(node.parent1))
        parents.push(state.nodesByName.get(node.parent1));
      if (node.parent2 !== "Nie dotyczy" && state.nodesByName.has(node.parent2))
        parents.push(state.nodesByName.get(node.parent2));
      toVisit.unshift(...parents.slice().reverse());
    }
  }

  let activePredecessors = [];
  if (ACTIVE_PREDECESSORS) {
    for (const p of predecessors) {
      const children = state.childrenDict[p.pk][1].map((childPk) =>
        state.nodesByPK.get(childPk.toString())
      );
      const activeDescendants = children.filter(
        (d) => ["A", "M"].includes(d.aktywnosc) && visited.has(d)
      );
      activePredecessors.push(...activeDescendants);
    }
    activePredecessors.sort((a, b) => (a.year >= b.year ? 1 : -1));
    const finalActivePredecessors = [];
    for (let i = activePredecessors.length - 1; i >= 0; i--) {
      const p = activePredecessors[i];
      let isNotChild = true;
      for (let j = i - 1; j >= 0; j--) {
        const potentialParent = activePredecessors[j];
        if (
          state.childrenDict[potentialParent.pk][1].includes(parseInt(p.pk, 10))
        ) {
          isNotChild = false;
          break;
        }
      }
      if (isNotChild) finalActivePredecessors.push(p);
    }
    return finalActivePredecessors;
  }
  return predecessors;
}

export function getDescendants(pk, childrenDict, acc = new Set()) {
  const entry = childrenDict[pk];
  if (!entry) return acc;
  const children = entry[1] || [];
  for (const childPk of children) {
    if (!acc.has(childPk)) {
      acc.add(childPk.toString());
      getDescendants(childPk, childrenDict, acc);
    }
  }
  return acc;
}

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
