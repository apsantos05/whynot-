const fs = require('fs'), path = require('path');
const { PNG } = require('pngjs');
const { writePsdBuffer } = require('ag-psd');
const [manifestPath, outDir] = process.argv.slice(2);
const man = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const load = f => { const p = PNG.sync.read(fs.readFileSync(f)); return { width: p.width, height: p.height, data: new Uint8ClampedArray(p.data) }; };
const hex = h => ({ r: parseInt(h.slice(1, 3), 16), g: parseInt(h.slice(3, 5), 16), b: parseInt(h.slice(5, 7), 16) });
for (const [doc, m] of Object.entries(man)) {
  const children = m.layers.map(L => {
    const layer = { name: L.name, imageData: load(L.png), left: 0, top: 0 };
    if (L.blend) layer.blendMode = L.blend;
    if (L.opacity != null && L.opacity !== 1) layer.opacity = L.opacity;
    if (L.text) {
      const t = L.text;
      layer.text = {
        text: t.text,
        transform: [1, 0, 0, 1, t.x, t.y],
        antiAlias: 'smooth',
        style: { font: { name: t.font }, fontSize: t.size, fillColor: hex(t.color), tracking: Math.round(t.ls * 1000), autoLeading: true },
        paragraphStyle: { justification: t.anchor === 'middle' ? 'center' : 'left' },
      };
    }
    return layer;
  });
  const psd = { width: m.width, height: m.height, children, imageData: load(path.join(path.dirname(m.layers[0].png), '_composite.png')) };
  const out = path.join(outDir, doc + '.psd');
  fs.writeFileSync(out, writePsdBuffer(psd, { generateThumbnail: false, invalidateTextLayers: false, compress: true }));
  console.log('ok', out);
}
