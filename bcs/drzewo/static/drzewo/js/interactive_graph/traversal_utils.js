export function getPredecessors(state, ACTIVE_PREDECESSORS, YEARS_BACK) {
  const years = Object.keys(state.years)
    .filter((year) => year !== "BEAN")
    .map((y) => parseInt(y, 10));
  const currentYear = Math.max(...years);

  const toVisit = state.nodes.filter(
    (node) =>
      node.year &&
      parseInt(node.year, 10) > currentYear - YEARS_BACK &&
      ["A", "M"].includes(node.aktywnosc)
  );
  let predecessors = [];
  const visited = new Set();

  while (toVisit.length > 0) {
    const node = toVisit.pop();
    if (node === undefined) continue; // onp=true case
    if (visited.has(node)) continue;
    visited.add(node);
    if (["N", "O"].includes(node.aktywnosc)) {
      predecessors.push(node);
    } else {
      const parents = [];
      if (node.parent1 !== "0") parents.push(state.nodesByPK.get(node.parent1));
      if (node.parent2 !== "0") parents.push(state.nodesByPK.get(node.parent2));
      toVisit.unshift(...parents);
    }
  }

  predecessors = [...new Set(predecessors)];

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
    activePredecessors = [...new Set(activePredecessors)];
    activePredecessors.sort((a, b) => (a.year >= b.year ? 1 : -1));
    const finalActivePredecessors = [];
    for (let idx in activePredecessors.toReversed()) {
      const p = activePredecessors[idx];
      let isNotChild = true;
      for (let i = idx - 1; i >= 0; i--) {
        const potentialParent = activePredecessors[i];
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
