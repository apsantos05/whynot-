// Monta no Photoshop a arte das promoters do afterzin a partir das camadas em ./camadas
// e salva PSD (camadas editáveis) + PNG na pasta acima. Rodar por Arquivo > Scripts > Procurar...
#target photoshop
app.displayDialogs = DialogModes.NO;
var pasta = File($.fileName).parent;
var cam = Folder(pasta + '/camadas');
var prefs = app.preferences.rulerUnits; app.preferences.rulerUnits = Units.PIXELS;

var doc = app.documents.add(1080, 1920, 72, 'afterzin_promoters', NewDocumentMode.RGB, DocumentFill.TRANSPARENT);

function poe(nome, rotulo, grupo) {
    var f = File(cam + '/' + nome + '.png'); if (!f.exists) return null;
    var src = app.open(f);
    src.activeLayer.duplicate(grupo ? grupo : doc, ElementPlacement.PLACEATBEGINNING);
    src.close(SaveOptions.DONOTSAVECHANGES);
    app.activeDocument = doc;
    var l = doc.activeLayer; l.name = rotulo; return l;
}
function curvas(nome, pontos) {      // camada de ajuste de Curvas (RGB) logo acima da ativa
    var d = new ActionDescriptor(), r = new ActionReference(); r.putClass(stringIDToTypeID('adjustmentLayer')); d.putReference(charIDToTypeID('null'), r);
    var u = new ActionDescriptor(); u.putString(charIDToTypeID('Nm  '), nome);
    var c = new ActionDescriptor(); c.putEnumerated(stringIDToTypeID('presetKind'), stringIDToTypeID('presetKindType'), stringIDToTypeID('presetKindCustom'));
    var lst = new ActionList(), ad = new ActionDescriptor(), rr = new ActionReference();
    rr.putEnumerated(charIDToTypeID('Chnl'), charIDToTypeID('Chnl'), charIDToTypeID('Cmps')); ad.putReference(charIDToTypeID('Chnl'), rr);
    var pl = new ActionList();
    for (var i = 0; i < pontos.length; i++) { var p = new ActionDescriptor(); p.putDouble(charIDToTypeID('Hrzn'), pontos[i][0]); p.putDouble(charIDToTypeID('Vrtc'), pontos[i][1]); pl.putObject(charIDToTypeID('Pnt '), p); }
    ad.putList(charIDToTypeID('Crv '), pl); lst.putObject(charIDToTypeID('CrvA'), ad); c.putList(charIDToTypeID('Adjs'), lst);
    u.putObject(charIDToTypeID('Type'), charIDToTypeID('Crvs'), c); d.putObject(charIDToTypeID('Usng'), charIDToTypeID('AdjL'), u);
    executeAction(charIDToTypeID('Mk  '), d, DialogModes.NO);
}
function recorta() { executeAction(stringIDToTypeID('groupEvent'), new ActionDescriptor(), DialogModes.NO); }   // clipping mask na camada de baixo

var fundo = poe('fundo_pb', 'fundo P&B (feixes de luz)');
var djs = doc.layerSets.add(); djs.name = 'DJs (cor natural)'; djs.move(fundo, ElementPlacement.PLACEBEFORE);
var ordem = [['dj_mexikanno', 'Mexikanno'], ['dj_marquez', 'Marquez'], ['dj_possani', 'Possani'], ['dj_polao', 'Polão'],
             ['sombra_frente', 'sombra da frente'], ['dj_kaio-alves', 'Kaio Alves'], ['dj_paganotti', 'Paganotti'], ['veu_texto', 'véu atrás dos nomes']];
for (var i = 0; i < ordem.length; i++) {
    var l = poe(ordem[i][0], ordem[i][1], djs);
    if (ordem[i][0] == 'sombra_frente') { l.opacity = 75; continue; }
    if (ordem[i][0] == 'veu_texto') continue;
    // contraste leve só nesse DJ (curva em S presa na camada)
    curvas('contraste ' + ordem[i][1], [[0, 0], [64, 58], [192, 200], [255, 255]]); recorta();
}
// dá unidade às 6 fotos: leve calor + brilho do grupo todo
app.activeDocument.activeLayer = djs;
var txt = doc.layerSets.add(); txt.name = 'textos'; txt.move(djs, ElementPlacement.PLACEBEFORE);
var t = [['txt_topo', 'logo e line-up'], ['txt_titulo', 'afterzin + data'], ['txt_nomes', 'nomes'], ['txt_ingresso', 'link de ingresso aqui']];
for (var k = 0; k < t.length; k++) poe(t[k][0], t[k][1], txt);

// fundo preto embaixo de tudo
var base = doc.artLayers.add(); base.name = 'preto'; base.move(fundo, ElementPlacement.PLACEAFTER);
doc.selection.selectAll(); var cor = new SolidColor(); cor.rgb.red = 8; cor.rgb.green = 9; cor.rgb.blue = 10; doc.selection.fill(cor); doc.selection.deselect();

var psd = new PhotoshopSaveOptions(); psd.layers = true; psd.embedColorProfile = true;
doc.saveAs(File(pasta + '/afterzin_promoters.psd'), psd, true);
var png = new PNGSaveOptions(); png.compression = 6;
doc.saveAs(File(pasta + '/afterzin_promoters.png'), png, true, Extension.LOWERCASE);
app.preferences.rulerUnits = prefs;
