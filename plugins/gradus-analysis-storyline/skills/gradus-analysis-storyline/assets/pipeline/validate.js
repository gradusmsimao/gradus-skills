// Valida o deck novo em Chrome headless (puppeteer-core).
const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const FILE = path.resolve(__dirname, '..', 'Magalu_DeckTV_MidiaOffline_v1.html');
const SHOTS = path.resolve(__dirname, 'shots');
if (!fs.existsSync(SHOTS)) fs.mkdirSync(SHOTS, { recursive: true });

(async () => {
  const errors = [];
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-gpu', '--window-size=1366,820']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1366, height: 820, deviceScaleFactor: 2 });
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  const url = 'file:///' + FILE.replace(/\\/g, '/');
  await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
  await new Promise(r => setTimeout(r, 400));

  const info = await page.evaluate(() => {
    const ss = Array.from(document.querySelectorAll('.slide'));
    return { total: ss.length, ids: ss.map(s => s.dataset.id) };
  });

  const report = [];
  for (let i = 0; i < info.total; i++) {
    if (i === 0) {
      // garante slide 0 ativo no load
    } else {
      // navega pelo botão real "Próximo →" (dispara renderActive interno)
      // btn-next usa nextMain() que pula data-backup; aqui não há backup, então anda 1 a 1
      await page.click('#btn-next');
    }
    await new Promise(r => setTimeout(r, 380));
    const m = await page.evaluate(() => {
      const s = document.querySelector('.slide.active');
      return { id: s.dataset.id, sh: s.scrollHeight };
    });
    const overflow = m.sh > 728;
    report.push({ idx: i + 1, id: m.id, scrollHeight: m.sh, overflow });
    const fn = path.join(SHOTS, `slide-${String(i + 1).padStart(2, '0')}-${m.id}.png`);
    await page.screenshot({ path: fn });
  }

  await browser.close();

  const overflowCount = report.filter(r => r.overflow).length;
  const out = {
    file: path.basename(FILE),
    totalSlides: info.total,
    ids: info.ids,
    overflowCount,
    errorCount: errors.length,
    errors,
    slides: report
  };
  fs.writeFileSync(path.join(__dirname, 'validate-report.json'), JSON.stringify(out, null, 2), 'utf8');
  console.log(JSON.stringify(out, null, 2));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
