import { LCM, vectorGCD } from "/static/js/math.js";

export function changeOpacity(nodeLayer, conditionFunc, opacity) {
  nodeLayer
    .selectAll("g.node circle")
    .style("opacity", (d) => (conditionFunc(d) ? opacity : 1));
  nodeLayer
    .selectAll("g.node text")
    .style("opacity", (d) => (conditionFunc(d) ? opacity : 1));
}

export function applyGradient(
  gradientMap,
  modifier,
  nodeAttribute,
  fallbackProc,
  defs,
  state
) {
  gradientMap.forEach((gradientVector, nodePK) => {
    const patId = `grad-${nodePK}`;

    // Remove old pattern if exists
    defs.select(`#${patId}`).remove();

    // Create a pattern that maps a unit circle
    const pattern = defs
      .append("pattern")
      .attr("id", patId)
      .attr("patternUnits", "objectBoundingBox")
      .attr("width", 1)
      .attr("height", 1)
      .attr("viewBox", "-1 -1 2 2"); // center (-1,-1) to (1,1)

    // Build pie slices
    const total = gradientVector.reduce((a, b) => a + b, 0);
    let angleStart = 0;

    gradientVector.forEach((value, i) => {
      const portion = value / total;
      const angleEnd = angleStart + portion * Math.PI * 2;
      const color = `hsl(${i * modifier}, 70%, 55%)`;

      pattern
        .append("path")
        .attr("d", describeArc(0, 0, 1, angleStart, angleEnd))
        .attr("fill", color);

      angleStart = angleEnd;
    });
  });

  // Assign fills to nodes
  state.nodes.forEach((node) => {
    if (gradientMap.has(node[nodeAttribute])) {
      node.gradient = `url(#grad-${node[nodeAttribute]})`;
    } else {
      fallbackProc(node);
    }
  });
}

// Arc generator - creates wedge paths
function describeArc(cx, cy, r, startAngle, endAngle) {
  const x1 = cx + r * Math.cos(startAngle);
  const y1 = cy + r * Math.sin(startAngle);
  const x2 = cx + r * Math.cos(endAngle);
  const y2 = cy + r * Math.sin(endAngle);

  const largeArc = endAngle - startAngle > Math.PI ? 1 : 0;

  return `
    M ${cx} ${cy}
    L ${x1} ${y1}
    A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}
    Z
  `;
}


export function gradientMapUpdate(pk, childrenDict, gradientMap, map) {
  const node = map.get(pk.toString());
  const parentGradient = gradientMap.get(pk);
  const lastIdx = parentGradient.length - 1;
  const entry = childrenDict[pk];
  const children = entry?.[1] || [];
  for (const childPK of children) {
    const child = map.get(childPK.toString());
    if (gradientMap.has(childPK.toString())) {
      // new parent, combine gradients
      const firstParentGradient = gradientMap.get(childPK.toString());
      let finalGradient;
      if (firstParentGradient[lastIdx] !== pk) {
        finalGradient = propagateGradient(
          firstParentGradient.slice(0, lastIdx),
          parentGradient.slice(0, lastIdx)
        );
        finalGradient.push(pk);
      } else {
        // same parent, copy parent's gradient
        finalGradient = [...parentGradient];
        finalGradient[lastIdx] = pk;
      }
      gradientMap.set(childPK.toString(), [...finalGradient]);
    } else {
      // first occurrence, copy parent's gradient
      const finalGradient = [...parentGradient];
      finalGradient[lastIdx] = pk;
      gradientMap.set(childPK.toString(), [...finalGradient]);
    }
    gradientMapUpdate(childPK.toString(), childrenDict, gradientMap, map);
  }
}

export function propagateGradient(firstParentGradient, secondParentGradient) {
  const A = firstParentGradient;
  const B = secondParentGradient;
  const A_sum = A.reduce((a, b) => a + b, 0);
  if (A_sum === 0) return B;
  const B_sum = B.reduce((a, b) => a + b, 0);
  if (B_sum === 0) return A;
  const lcm = LCM(A_sum, B_sum);
  const A_modifier = lcm / A_sum;
  const B_modifier = lcm / B_sum;
  const gradient = A.map(
    (A_value, i) => A_modifier * A_value + B_modifier * B[i]
  );
  const gcd = vectorGCD(gradient);
  return gradient.map((v) => v / gcd);
}
