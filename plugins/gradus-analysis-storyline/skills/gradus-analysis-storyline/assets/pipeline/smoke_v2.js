// Smoke-test interativo da arquitetura v2 no deck de TV.
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
  await new Promise(r => setTimeout(r, 400));

  const r = {};
  // 1. estado inicial = present
  r.modeInicial = await p.evaluate(() => document.body.dataset.mode);
  r.toolsEscondidoInicial = await p.evaluate(() => document.getElementById('hdr-tools').classList.contains('hidden'));
  r.leadEditavelInicial = await p.evaluate(() => document.querySelector('.slide .lead').getAttribute('contenteditable'));

  // 2. clica em Editar
  await p.click('#btn-mode'); await new Promise(r => setTimeout(r, 150));
  r.modeAposToggle = await p.evaluate(() => document.body.dataset.mode);
  r.toolsVisivelEdit = await p.evaluate(() => !document.getElementById('hdr-tools').classList.contains('hidden'));
  r.leadEditavelEdit = await p.evaluate(() => document.querySelector('.slide .lead').getAttribute('contenteditable'));
  // número de tabela NÃO deve virar editável
  r.numTabelaEditavel = await p.evaluate(() => { const td = document.querySelector('.slide.active .tbl td.num') || document.querySelector('.tbl td.num'); return td ? td.getAttribute('contenteditable') : 'sem-tabela-no-slide'; });

  // 3. +Bubble adiciona no slide ativo — navega (btn-next move o idx real) até sair da capa
  for (let i = 0; i < 5; i++) { await p.click('#btn-next'); await new Promise(r => setTimeout(r, 80)); }
  r.slideAtivoPraBubble = await p.evaluate(() => document.querySelector('.slide.active').dataset.id);
  const antes = await p.evaluate(() => document.querySelectorAll('.callout-opp.custom-navy').length);
  await p.click('#btn-bubble'); await new Promise(r => setTimeout(r, 150));
  const depois = await p.evaluate(() => document.querySelectorAll('.callout-opp.custom-navy').length);
  r.bubbleAdicionado = depois === antes + 1;

  // 4. volta pra present
  await p.click('#btn-mode'); await new Promise(r => setTimeout(r, 150));
  r.modeVoltou = await p.evaluate(() => document.body.dataset.mode);
  r.toolsEscondidoFinal = await p.evaluate(() => document.getElementById('hdr-tools').classList.contains('hidden'));

  r.erros = errs;
  console.log(JSON.stringify(r, null, 2));
  await b.close();
})().catch(e => { console.error('FATAL', e); process.exit(1); });
