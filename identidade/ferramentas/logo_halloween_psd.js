const fs = require('fs'), path = require('path');
const { PNG } = require('pngjs');

const { writePsdBuffer } = require('ag-psd');
const [dir, out] = process.argv.slice(2);
const load = f => { const p = PNG.sync.read(fs.readFileSync(path.join(dir, f))); return { width: p.width, height: p.height, data: new Uint8ClampedArray(p.data) }; };
const L = (name, f, extra = {}) => ({ name, imageData: load(f), ...extra });
const files = fs.readdirSync(dir).filter(f => f.endsWith('.png')).sort();
const ext = files.filter(f => f.includes('extrusao')).map(f => L('Extrusão ' + f.slice(-6, -4), f));
const psd = {
  width: 2160, height: 2160,
  children: [
    L('Fundo (preto brasa + brilho)', '00_fundo.png'),
    { name: 'Extrusão 3D (12 degraus, brasa)', opened: false, children: ext },
    L('Letras · osso #efe4d0', '13_letras_osso.png'),
    L('Brilho da abóbora', '14_brilho_abobora.png', { blendMode: 'screen' }),
    L('Abóbora (no lugar do o)', '15_abobora.png'),
  ],
};
psd.imageData = (()=>{const p=PNG.sync.read(fs.readFileSync(path.join(dir,'../composite_inclinado.png')));return {width:p.width,height:p.height,data:new Uint8ClampedArray(p.data)}})(); // composite fallback
fs.writeFileSync(out, writePsdBuffer(psd, { generateThumbnail: false }));
console.log('ok', out);
