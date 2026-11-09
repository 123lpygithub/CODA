// Capture the six paper figures from an isolated API serving demonstration runs.
// NODE_PATH may point to a separate Playwright installation.
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');

const baseUrl = process.env.CODA_CAPTURE_URL || 'http://127.0.0.1:5176';
const output = path.resolve(process.env.CODA_CAPTURE_OUTPUT || '../images');
const viewport = { width: 1280, height: 1320 };

async function selectRun(page, runId) {
  await page.locator('.run-picker-trigger').click();
  const options = page.locator('.run-option');
  await options.first().waitFor();
  for (let index = 0; index < await options.count(); index++) {
    const option = options.nth(index);
    const label = (await option.innerText()).replace(/\s+/g, ' ').trim();
    if (label === runId || label.startsWith(`${runId} `)) {
      await option.click();
      await page.locator('.execution-phase.active').waitFor();
      await page.waitForTimeout(650);
      return;
    }
  }
  throw new Error(`Demonstration run not found: ${runId}`);
}

async function selectNode(page, name) {
  await page.locator('.execution-phase-node').filter({ hasText: name }).first().click();
  await page.waitForTimeout(250);
}

async function focus(page, selector, offset = 0) {
  await page.locator(selector).first().evaluate((element, inset) => {
    window.scrollTo(0, window.scrollY + element.getBoundingClientRect().top - inset);
  }, offset);
  await page.waitForTimeout(200);
}

async function capture(page, filename) {
  await page.mouse.move(viewport.width - 1, 0);
  await page.locator('.workflow-sidebar').evaluate(element => { element.scrollTop = 0; });
  const sidebar = await page.locator('.workflow-sidebar').boundingBox();
  const lastPhase = await page.locator('.execution-phase').last().boundingBox();
  if (!sidebar || !lastPhase || lastPhase.y + lastPhase.height > viewport.height) {
    throw new Error(`The complete execution path must be visible in ${filename}`);
  }
  const y = Math.max(0, Math.ceil(sidebar.y));
  const height = Math.floor(Math.min(viewport.height - y, sidebar.height));
  await page.screenshot({ path: path.join(output, filename), clip: { x: 0, y, width: viewport.width, height } });
  const activePhase = await page.locator('.execution-phase.active > header').innerText();
  console.log(`${filename}: ${viewport.width} x ${height} CSS pixels; ${activePhase.replace(/\s+/g, ' ')}`);
}

async function main() {
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CODA_CHROMIUM_PATH ? { executablePath: process.env.CODA_CHROMIUM_PATH } : {}),
    args: ['--no-sandbox'],
  });
  try {
    const page = await browser.newPage({ viewport, deviceScaleFactor: 2 });
    const failures = [];
    page.on('pageerror', error => failures.push(error.message));
    await page.addInitScript(() => localStorage.setItem('coda-language', 'en'));
    // The capture should never launch agents or submit a research decision.
    await page.route('**/api/runs/**', route => {
      const request = route.request();
      if (request.method() !== 'GET' && !request.url().includes('/review-timer')) {
        return route.abort('blockedbyclient');
      }
      return route.continue();
    });
    await page.goto(baseUrl, { waitUntil: 'domcontentloaded' });
    await page.locator('.run-picker-trigger').waitFor();
    await page.evaluate(() => document.fonts.ready);

    await selectRun(page, 'run-1ccda356300e');
    await selectNode(page, 'Familiarization');
    await focus(page, '.process-workspace');
    await capture(page, 'workbench-stage-1-familiarization.png');
    await selectNode(page, 'Initial coding');
    await focus(page, '.process-workspace');
    await capture(page, 'workbench-stage-2-initial-coding.png');
    await selectNode(page, 'Constant comparison');
    await focus(page, '.process-count', 95);
    await capture(page, 'workbench-stage-4-iterative-coding.png');
    await selectNode(page, 'Triggered review gate');
    const reveal = page.getByRole('button', { name: /Reveal evidence packet/i });
    if (await reveal.isVisible()) {
      await page.locator('.review-panel textarea').first().fill(
        'The task requires the longest palindromic suffix; check whether the implementation searches suffixes rather than prefixes.',
      );
      await reveal.click();
    }
    await focus(page, '.review-form .form-section:nth-child(4)', 75);
    await capture(page, 'workbench-stage-5-codebook-refinement.png');

    await selectRun(page, 'run-initial-review-capture');
    await focus(page, '.process-workspace');
    await capture(page, 'workbench-stage-3-initial-categorization.png');
    await selectRun(page, 'run-final-review-capture');
    await focus(page, '.stage-review-audit:has(.stage-facts)', 95);
    await capture(page, 'workbench-stage-6-stabilization-audit.png');

    if (failures.length) throw new Error(failures.join('\n'));
    console.log('Captured all six stages without submitting review decisions.');
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
