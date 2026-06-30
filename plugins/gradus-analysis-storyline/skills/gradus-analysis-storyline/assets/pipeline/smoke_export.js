// Smoke-test do export de dados por elemento no template v2.
const puppeteer = require('puppeteer-core');
const path = require('path');
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const FILE = path.resolve(__dirname, '..', 'deck-template-v2.html');
(async () => {
  const errs = [];
  const b = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args: ['--no-sandbox'] });
  const p = await b.newPage();
  p.on('pageerror', e => errs.push('PAGEERR: ' + e.message));
  p.on('console', m => { if (m.type() === 'error') errs.push('CONSOLE: ' + m.text()); });
  await p.goto('file:///' + FILE.replace(/\\/g, '/'), { waitUntil: 'networkidle0' });
  await new Promise(r => setTimeout(r, 400));
  const r = {};
  r.xlsxLoaded = await p.evaluate(() => typeof XLSX !== 'undefined' && !!XLSX.utils);
  r.exportButtonsCount = await p.evaluate(() => document.querySelectorAll('.el-export').length);
  // present mode: botões escondidos
  r.hiddenInPresent = await p.evaluate(() => {
    const els = [...document.querySelectorAll('.el-export')];
    return els.every(e => getComputedStyle(e).display === 'none');
  });
  // edit mode: botões existem (display controlado por :hover, então testamos a regra CSS via classes do body)
  await p.click('#btn-mode'); await new Promise(r => setTimeout(r, 120));
  r.bodyModeEdit = await p.evaluate(() => document.body.dataset.mode);
  r.layersTemExport = await p.evaluate(() => document.body.dataset.layers.includes('export'));
  // testa a montagem do workbook a partir de uma TABELA real (sem baixar): replica tableToAoA + book
  r.tabelaAoA = await p.evaluate(() => {
    const tbl = document.querySelector('.slide#x, table'); // primeira tabela do doc
    const t = document.querySelector('.exportable table');
    if (!t || typeof XLSX === 'undefined') return null;
    // usa a própria função da página
    const aoa = (typeof tableToAoA === 'function') ? tableToAoA(t) : null;
    if (!aoa) return 'sem tableToAoA';
    // monta wb e serializa pra string (prova que escreve sem erro), sem disparar download
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(aoa), 'Dados');
    const out = XLSX.write(wb, { bookType: 'xlsx', type: 'base64' });
    return { linhas: aoa.length, colsPrimeira: aoa[0] ? aoa[0].length : 0, base64len: out.length };
  });
  // testa export de SÉRIE de gráfico (data-export-series)
  r.serieAoA = await p.evaluate(() => {
    const el = document.querySelector('[data-export-series]');
    if (!el) return 'sem data-export-series';
    const s = JSON.parse(el.getAttribute('data-export-series'));
    return { cols: s.cols, rows: (s.rows || []).length };
  });
  r.erros = errs;
  console.log(JSON.stringify(r, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
