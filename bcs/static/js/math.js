export function LCM(a, b) {
  return (b / GCD(a, b)) * a;
}

export function GCD(a, b) {
  if (a === 0) return b;
  if (b === 0) return a;
  let k;
  for (k = 0; ((a | b) & 1) === 0; ++k) {
    a >>= 1;
    b >>= 1;
  }
  while ((a & 1) === 0) a >>= 1;
  do {
    while ((b & 1) === 0) b >>= 1;
    if (a > b) [a, b] = [b, a];
    b -= a;
  } while (b !== 0);
  return a << k;
}

export function vectorGCD(nonZeroVector) {
  function func(vector) {
    let first;
    let completed = true; // assume we complete the loop
    for (const n of vector) {
      if (n === 1) return 1;
      if (n !== 0) {
        if (first === undefined) first = n;
        else if (n !== first) {
          completed = false;
          break;
        }
      }
    }
    if (completed) return first;
    return 0;
  }

  function twoLargestIndices(vector) {
    let max1 = -Infinity,
      max2 = -Infinity;
    let idx1, idx2;
    vector.forEach((n, i) => {
      if (n > max1) {
        max2 = max1;
        idx2 = idx1;
        max1 = n;
        idx1 = i;
      } else if (n >= max2) {
        max2 = n;
        idx2 = i;
      }
    });
    return [idx1, idx2];
  }

  const v = [...nonZeroVector];
  let check = func(v);
  if (check !== 0) return check;

  let k = 0;
  while (v.every((n) => (n & 1) === 0)) {
    for (let i = 0; i < v.length; i++) v[i] >>= 1;
    k++;
  }
  for (let i = 0; i < v.length; i++) {
    if (v[i] !== 0) while ((v[i] & 1) === 0) v[i] >>= 1;
  }
  while (true) {
    check = func(v);
    if (check !== 0) return check << k;
    const [idx1, idx2] = twoLargestIndices(v);
    let n = v[idx1] - v[idx2];
    if (n !== 0) while ((n & 1) === 0) n >>= 1;
    v[idx1] = n;
  }
}
