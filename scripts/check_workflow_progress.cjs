// Read-only browser regression for initialization position and status labels.
// All run states are mocked; no model requests or saved-run mutations.
const {chromium} = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const base = process.env.CODA_CHECK_API || 'http://127.0.0.1:8013';
const url = process.env.CODA_CHECK_URL || 'http://127.0.0.1:5177';
const id = process.env.CODA_CHECK_RUN || 'run-1ccda356300e';

async function main() {
  const saved = await (await fetch(`${base}/api/runs/${id}`)).json();
  const browser = await chromium.launch({
    ...(process.env.CODA_CHROMIUM_PATH ? {executablePath: process.env.CODA_CHROMIUM_PATH} : {}),
    args: ['--no-sandbox'],
  });
  try {
    const page = await browser.newPage({viewport: {width:1440, height:1000}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.addInitScript(() => localStorage.setItem('coda-language', 'en'));
    let run;
    const setState = (status, phase, stage_index=0) => {
      run = {...saved, status:'not_started', bootstrap_status:status, codebook_version:0,
        reviewed_artifacts:0, human_reviewed_artifacts:0, total_artifacts:saved.input_artifacts,
        code_count:0, bootstrap_artifacts:0, bootstrap_code_count:0,
        bootstrap_progress:{...saved.bootstrap_progress, status, phase, stage_index, percent:0}};
    };
    await page.route('**/api/**', async route => {
      const request = route.request();
      assert.equal(request.method(), 'GET', 'This check must never write to a run');
      const parsed = new URL(request.url());
      if (parsed.pathname === '/api/runs') return route.fulfill({json:[run]});
      if (parsed.pathname === `/api/runs/${id}`) return route.fulfill({json:run});
      if (parsed.pathname.endsWith('/review-packet')) return route.fulfill({status:409, json:{detail:'Initialization required'}});
      return route.fulfill({response: await page.request.get(base + parsed.pathname + parsed.search)});
    });
    const selected = () => page.locator('.execution-phase-node[aria-current="step"]');
    for (const [status, phase, index, nodeIndex, title] of [
      ['not_run','pending',0,0,'Task created'],
      ['running','evidence',1,0,'Initialization in progress'],
      ['running','initial_coding',2,1,'Initialization in progress'],
      ['running','induction',3,2,'Initialization in progress'],
      ['running','validation',5,3,'Initialization in progress'],
      ['cancelled','cancelled',2,1,'Initialization paused'],
      ['interrupted','interrupted',3,2,'Initialization paused'],
      ['failed','failed',5,3,'Initialization failed'],
      ['cancelled','cancelled',0,0,'Initialization paused'],
    ]) {
      setState(status,phase,index);
      await page.goto(url);
      await page.locator('.task-setup-card h2').waitFor();
      assert((await page.locator('.task-setup-card h2').innerText()).includes(title));
      assert.equal(await page.locator('.execution-phase-node').nth(nodeIndex).getAttribute('aria-current'),'step');
      if (status === 'not_run') assert.equal(await page.locator('.process-stage-meta .workflow-status').innerText(),'Not started');
      if (status !== 'not_run') assert(!(await page.locator('.task-summary .run-status').innerText()).includes('Not started'));
      assert.equal(await selected().count(),1);
    }
    setState('running','evidence',1);
    await page.reload(); await selected().waitFor();
    setState('running','initial_coding',2);
    await page.waitForFunction(() => document.querySelectorAll('.execution-phase-node')[1].getAttribute('aria-current') === 'step');
    await page.locator('.execution-phase-node').nth(0).click();
    setState('running','induction',3);
    await page.waitForTimeout(1500);
    assert.equal(await page.locator('.execution-phase-node').nth(0).getAttribute('aria-current'),'step');
    setState('not_run','pending');
    await page.reload(); await page.locator('.task-setup-card').waitFor();
    const output = process.env.CODA_CHECK_OUTPUT || '/tmp/coda-workflow-progress';
    await fs.mkdir(output,{recursive:true});
    await page.screenshot({path:output+'/new-run.png'});
    assert.deepEqual(errors,[]);
    console.log(JSON.stringify({result:'PASS', checks:'New run starts at 01; phase mapping; paused/failed checkpoint positions; live progression; manual inspection preserved',errors}));
  } finally {await browser.close();}
}
main().catch(error => {console.error(error); process.exit(1)});
