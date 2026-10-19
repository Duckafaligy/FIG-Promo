// A small QR code maker for the admin's authenticator set-up (FIX-LIST #83): byte mode, error correction M, versions 1-10
// (up to 213 bytes; an otpauth link is about 110). Classic black squares on white, as an SVG string.
// ponytail: versions 1-10 and level M only; add rows to BLOCKS if a longer text ever needs it
// Checked against the qrcode package (the app's) in check.js: same modules for the same version and mask.

// per version (level M): [error-correction codewords per block, [blocks, data codewords each], ...]
const BLOCKS = [null, [10, [1, 16]], [16, [1, 28]], [26, [1, 44]], [18, [2, 32]], [24, [2, 43]], [16, [4, 27]], [18, [4, 31]],
  [22, [2, 38], [2, 39]], [22, [3, 36], [2, 37]], [26, [4, 43], [1, 44]]];
const ALIGN = [null, [], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50]];

// GF(256) with 0x11D, for the Reed-Solomon error correction
const EXP = new Array(512), LOG = new Array(256);
for (let i = 0, x = 1; i < 255; i++) { EXP[i] = x; LOG[x] = i; x <<= 1; if (x & 256) x ^= 0x11d; }
for (let i = 255; i < 512; i++) EXP[i] = EXP[i - 255];
const mul = (a, b) => (a && b ? EXP[LOG[a] + LOG[b]] : 0);
function ecc(data, n) {
  let gen = [1];
  for (let i = 0; i < n; i++) { const next = new Array(gen.length + 1).fill(0); gen.forEach((g, j) => { next[j] ^= g; next[j + 1] ^= mul(g, EXP[i]); }); gen = next; }
  const rem = new Array(n).fill(0);
  for (const d of data) { const f = d ^ rem.shift(); rem.push(0); for (let j = 0; j < n; j++) rem[j] ^= mul(gen[j + 1], f); }
  return rem;
}
const bch = (value, poly, bits) => { let v = value << bits; const top = 31 - Math.clz32(poly); while (31 - Math.clz32(v) >= top) v ^= poly << (31 - Math.clz32(v) - top); return (value << bits) | v; };

const MASKS = [(r, c) => (r + c) % 2 === 0, (r) => r % 2 === 0, (r, c) => c % 3 === 0, (r, c) => (r + c) % 3 === 0,
  (r, c) => (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0, (r, c) => ((r * c) % 2) + ((r * c) % 3) === 0,
  (r, c) => (((r * c) % 2) + ((r * c) % 3)) % 2 === 0, (r, c) => (((r + c) % 2) + ((r * c) % 3)) % 2 === 0];

/** The modules (true = dark) for a text: { size, dark: boolean[][] , version, mask }. */
function make(text, opts = {}) {
  const bytes = Buffer.from(String(text), "utf8");
  const cap = (v) => BLOCKS[v].slice(1).reduce((n, [b, d]) => n + b * d, 0);
  const version = opts.version || BLOCKS.findIndex((b, v) => v && cap(v) * 8 >= 4 + (v < 10 ? 8 : 16) + bytes.length * 8);
  if (version < 1 || !BLOCKS[version]) throw new Error("too long for a QR code here");
  // the data: mode 0100, the length, the bytes, then the end and the padding
  const bits = [];
  const put = (val, n) => { for (let i = n - 1; i >= 0; i--) bits.push((val >>> i) & 1); };
  put(4, 4); put(bytes.length, version < 10 ? 8 : 16); for (const b of bytes) put(b, 8);
  const total = cap(version) * 8;
  put(0, Math.min(4, total - bits.length)); while (bits.length % 8) bits.push(0);
  const data = [];
  for (let i = 0; i < bits.length; i += 8) data.push(parseInt(bits.slice(i, i + 8).join(""), 2));
  for (let pad = 0xec; data.length < total / 8; pad ^= 0xec ^ 0x11) data.push(pad);
  // split into blocks, add the error correction, interleave
  const [ecN, ...groups] = BLOCKS[version];
  const blocks = [];
  let at = 0;
  for (const [count, len] of groups) for (let i = 0; i < count; i++) { const d = data.slice(at, at + len); at += len; blocks.push({ d, e: ecc(d, ecN) }); }
  const out = [];
  for (let i = 0; i < Math.max(...blocks.map((b) => b.d.length)); i++) for (const b of blocks) if (i < b.d.length) out.push(b.d[i]);
  for (let i = 0; i < ecN; i++) for (const b of blocks) out.push(b.e[i]);

  const size = version * 4 + 17;
  const dark = Array.from({ length: size }, () => new Array(size).fill(false));
  const fixed = Array.from({ length: size }, () => new Array(size).fill(false));
  const set = (r, c, on) => { dark[r][c] = on; fixed[r][c] = true; };
  // finders and their white edges, timing, alignment, the dark module
  for (const [fr, fc] of [[0, 0], [0, size - 7], [size - 7, 0]])
    for (let r = -1; r <= 7; r++) for (let c = -1; c <= 7; c++) {
      const rr = fr + r, cc = fc + c;
      if (rr < 0 || cc < 0 || rr >= size || cc >= size) continue;
      const ring = Math.max(Math.abs(r - 3), Math.abs(c - 3));
      set(rr, cc, ring !== 2 && ring !== 4);
    }
  for (let i = 8; i < size - 8; i++) { set(6, i, i % 2 === 0); set(i, 6, i % 2 === 0); }
  const al = ALIGN[version];
  for (const r of al) for (const c of al) {
    if ((r === 6 && c === 6) || (r === 6 && c === al[al.length - 1]) || (r === al[al.length - 1] && c === 6)) continue;
    for (let i = -2; i <= 2; i++) for (let j = -2; j <= 2; j++) set(r + i, c + j, Math.max(Math.abs(i), Math.abs(j)) !== 1);
  }
  set(size - 8, 8, true);
  // reserve the format (and version) areas, filled in after the mask is chosen
  for (let i = 0; i < 9; i++) { fixed[8][i] = fixed[i][8] = true; }
  for (let i = 0; i < 8; i++) { fixed[8][size - 1 - i] = fixed[size - 1 - i][8] = true; }
  if (version >= 7) for (let i = 0; i < 6; i++) for (let j = 0; j < 3; j++) { fixed[i][size - 11 + j] = fixed[size - 11 + j][i] = true; }
  // the codewords, two columns at a time, up and down from the right
  let k = 0;
  for (let right = size - 1; right >= 1; right -= 2) {
    if (right === 6) right = 5;
    for (let vert = 0; vert < size; vert++) for (let j = 0; j < 2; j++) {
      const c = right - j, up = ((right + 1) & 2) === 0, r = up ? size - 1 - vert : vert;
      if (fixed[r][c]) continue;
      dark[r][c] = k < out.length * 8 ? ((out[k >>> 3] >>> (7 - (k & 7))) & 1) === 1 : false;
      k++;
    }
  }
  const finish = (mask) => {
    const m = dark.map((row, r) => row.map((on, c) => (fixed[r][c] ? on : on !== MASKS[mask](r, c))));
    const fmt = bch((0 << 3) | mask, 0x537, 10) ^ 0x5412; // level M = 00
    const fb = (i) => ((fmt >>> i) & 1) === 1;
    for (let i = 0; i <= 5; i++) m[i][8] = fb(i);
    m[7][8] = fb(6); m[8][8] = fb(7); m[8][7] = fb(8);
    for (let i = 9; i < 15; i++) m[8][14 - i] = fb(i);
    for (let i = 0; i < 8; i++) m[8][size - 1 - i] = fb(i);
    for (let i = 8; i < 15; i++) m[size - 15 + i][8] = fb(i);
    m[size - 8][8] = true;
    if (version >= 7) {
      const vb = bch(version, 0x1f25, 12);
      for (let i = 0; i < 18; i++) { const on = ((vb >>> i) & 1) === 1, a = size - 11 + (i % 3), b = Math.floor(i / 3); m[b][a] = on; m[a][b] = on; }
    }
    return m;
  };
  const mask = opts.mask ?? [0, 1, 2, 3, 4, 5, 6, 7].map((x) => [penalty(finish(x)), x]).sort((a, b) => a[0] - b[0])[0][1];
  return { size, dark: finish(mask), version, mask };
}

// the standard's four penalty rules, to pick the mask that scans best
function penalty(m) {
  const n = m.length;
  let p = 0;
  const runs = (line) => { let s = 0, len = 1; for (let i = 1; i <= line.length; i++) { if (i < line.length && line[i] === line[i - 1]) len++; else { if (len >= 5) s += len - 2; len = 1; } } return s; };
  const cols = m[0].map((_, c) => m.map((row) => row[c]));
  for (const line of [...m, ...cols]) {
    p += runs(line);
    const t = line.map((x) => (x ? 1 : 0)).join("");
    for (const pat of ["10111010000", "00001011101"]) for (let i = t.indexOf(pat); i >= 0; i = t.indexOf(pat, i + 1)) p += 40;
  }
  for (let r = 0; r < n - 1; r++) for (let c = 0; c < n - 1; c++) { const v = m[r][c]; if (v === m[r][c + 1] && v === m[r + 1][c] && v === m[r + 1][c + 1]) p += 3; }
  const darkN = m.flat().filter(Boolean).length;
  p += Math.floor(Math.abs(darkN * 20 - n * n * 10) / (n * n)) * 10;
  return p;
}

/** An SVG of the code with a 4-module white border. */
function svg(text, px = 220) {
  const { size, dark } = make(text);
  let d = "";
  dark.forEach((row, r) => row.forEach((on, c) => { if (on) d += `M${c + 4} ${r + 4}h1v1h-1z`; }));
  const n = size + 8;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${n} ${n}" width="${px}" height="${px}" shape-rendering="crispEdges" role="img" aria-label="QR code for your authenticator app"><rect width="${n}" height="${n}" fill="#fff"/><path d="${d}" fill="#000"/></svg>`;
}

module.exports = { make, svg };
