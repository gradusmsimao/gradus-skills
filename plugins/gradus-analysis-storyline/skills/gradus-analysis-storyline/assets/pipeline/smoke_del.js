// Testa criar e DELETAR bubble (× clicável fora de hover via .selected; + tecla Delete).
const puppeteer = require('puppeteer-core');
const path = require('path');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const FILE = path.resolve(__dirname, '..', 'Magalu_DeckTV_MidiaOffline_v1.html');
(async () => {
  const errs = [];
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage();
  p.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
  await p.setViewport({ width: 1366, height: 820, deviceScaleFactor: 1 });
  await p.goto('file:///' + FILE.replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 300));
  await p.click('#btn-mode'); await new Promise(r => setTimeout(r, 80));
  for (let i = 0; i < 5; i++) { await p.click('#btn-next'); await new Promise(r => setTimeout(r, 50)); }
  const r = {};

  // --- TESTE A: deletar pelo × (clicando de verdade na posição do botão) ---
  await p.click('#btn-bubble'); await new Promise(r => setTimeout(r, 100));
  r.addA = await p.evaluate(() => document.querySelectorAll('.callout-opp.custom-navy').length);
  // × está visível pq o bubble nasce .selected. Clica no centro do ×.
  const delBox = await p.evaluate(() => {
    const del = document.querySelector('.slide.active .callout-opp.custom-navy .bubble-del');
    if (!del) return null; const r = del.getBoundingClientRect();
    return { x: r.x + r.width / 2, y: r.y + r.height / 2, vis: getComputedStyle(del).display };
  });
  r.delVisivelSemHover = delBox && delBox.vis !== 'none';
  if (delBox) { await p.mouse.click(delBox.x, delBox.y); await new Promise(r => setTimeout(r, 100)); }
  r.depoisClickX = await p.evaluate(() => document.querySelectorAll('.callout-opp.custom-navy').length);

  // --- TESTE B: deletar pela tecla Delete (bubble selecionado, sem digitar) ---
  await p.click('#btn-bubble'); await new Promise(r => setTimeout(r, 100));
  r.addB = await p.evaluate(() => document.querySelectorAll('.callout-opp.custom-navy').length);
  // tira o foco do texto (senão Delete edita) — clica no corpo do bubble, não no texto
  await p.evaluate(() => { const b = document.querySelector('.slide.active .callout-opp.custom-navy'); b.classList.add('selected'); if(document.activeElement) document.activeElement.blur(); });
  await p.keyboard.press('Delete'); await new Promise(r => setTimeout(r, 100));
  r.depoisDelete = await p.evaluate(() => document.querySelectorAll('.callout-opp.custom-navy').length);

  r.erros = errs;
  console.log(JSON.stringify(r, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
