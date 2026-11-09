// Single-workspace browser regression: read an existing demonstration run, then
// simulate state changes through API contracts. All POSTs are mocked.
// Requires Playwright (may be supplied through NODE_PATH), a frontend configured
// for CODA_CHECK_API, and CODA_CHECK_RUN pointing to a demonstration run with
// a prepared case packet and completed bootstrap. No API key is needed.
// Optional: CODA_CHECK_URL, CODA_CHECK_OUTPUT, CODA_CHROMIUM_PATH.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const base=process.env.CODA_CHECK_API || 'http://127.0.0.1:8013';
const url=process.env.CODA_CHECK_URL || 'http://127.0.0.1:5177';
const id=process.env.CODA_CHECK_RUN || 'run-1ccda356300e';
const executablePath=process.env.CODA_CHROMIUM_PATH;
const clone=x=>JSON.parse(JSON.stringify(x));
async function main(){
 const output=process.env.CODA_CHECK_OUTPUT || '/tmp/coda-unified-ui';await fs.mkdir(output,{recursive:true});
 const get=async p=>{const r=await fetch(base+p);if(!r.ok)throw Error(p+': '+r.status);return r.json()};
 const datasets=await get('/api/datasets'), saved=await get('/api/runs/'+id), current=await get('/api/runs/'+id+'/current-artifact'), codebook=await get('/api/runs/'+id+'/codebook'), packet=await get('/api/runs/'+id+'/review-packet'), initial=await get('/api/runs/'+id+'/stage-reviews/initial?inspection=true'), final={...clone(initial),kind:'final',bootstrap:null,sampled_artifacts:[],initial_codings:[],coverage:{processed_artifacts:16,input_artifacts:16,bootstrap_artifacts:4,iterative_artifacts:12,code_count:14,low_frequency_codes:[]}}, history=await get('/api/runs/'+id+'/history'), artifacts=await get('/api/runs/'+id+'/artifacts');
 const browser=await chromium.launch({...(executablePath ? {executablePath} : {}),args:['--no-sandbox']});const errors=[];const failures=[];const passed=[];
 const page=await browser.newPage({viewport:{width:1440,height:1000}});page.on('pageerror',error=>errors.push(error.message));page.on('response',r=>{if(r.url().includes('/api/')&&r.status()>=400 && !r.url().endsWith('/review-packet')) failures.push(`${r.status()} ${r.url()}`)});
 // Read real fixture content; mock all timer writes. Never invoke agents or save decisions.
 await page.route('**/api/**',async route=>{if(route.request().url().includes('/review-timer'))return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({run:saved})});if(route.request().method()!=='GET')throw Error('Unexpected mutation in read-only test: '+route.request().url());await route.continue()});
 await page.addInitScript(()=>localStorage.setItem('coda-language','en'));
 await page.goto(url);await page.locator('.review-panel textarea').first().waitFor();
 assert.equal(await page.locator('.workbench-mode-switch').count(),0);assert.equal(await page.locator('.process-workspace').count(),1);assert.equal(await page.locator('.workspace').count(),0);
 assert((await page.locator('.topbar').boundingBox()).height<=72);
 await page.locator('.review-original pre').waitFor();await page.locator('.review-panel textarea').first().fill('Keep this observation while checking source and codebook.');
 await page.locator('.review-materials button').first().click();await page.locator('dialog[open]').waitFor();assert((await page.locator('dialog pre').innerText()).includes(packet.review_input.artifact.content.slice(0, 60)));await page.keyboard.press('Escape');await page.locator('dialog').waitFor({state:'detached'});
 await page.locator('.workspace-tools > summary').click();await page.locator('.workspace-tools button').filter({hasText:/^Codebook$/}).click();await page.locator('.codebook-browser:visible .code-item').first().click();await page.locator('.code-artifacts-detail:visible h3').waitFor();
 await page.locator('.codebook-browser:visible input').fill('no-such-concept-xyz');await page.waitForTimeout(100);assert.equal(await page.locator('.codebook-browser:visible .code-item').count(),0);await page.locator('.codebook-browser:visible input').fill('');
 for(const name of ['Review history','Codebook evolution','Retrospective recoding','Context requests','Bootstrap record','Run artifacts']){
  await page.locator('.workspace-tools button').filter({hasText:name}).click();await page.waitForTimeout(100);assert(await page.locator('.workflow-sidebar').isVisible());
 }
 await page.locator('.tool-heading button').click();assert.equal(await page.locator('.review-panel textarea').first().inputValue(),'Keep this observation while checking source and codebook.');
 await page.getByRole('button',{name:'Reveal evidence packet',exact:true}).click();
 for(const node of ['comparison','validation','iterative_context','iterative_coding']){const order={iterative_context:6,iterative_coding:7,comparison:8,validation:9}; await page.locator('.execution-phase-node').nth(order[node]).click();await page.waitForTimeout(100);assert(!(await page.locator('.workflow-stage-content').innerText()).includes('recordPreRead'));}
 // Bootstrap content must use bootstrap cases and bootstrap codebook, not the current case.
 await page.locator('.execution-phase-node').nth(0).click();await page.locator('.workflow-stage-content .process-output-card').first().waitFor();assert(!(await page.locator('.workflow-stage-content').innerText()).includes(`Artifact ${packet.artifact_id}`));
 await page.locator('.execution-phase-node').nth(2).click();await page.locator('.workflow-stage-content .process-output-card').first().waitFor();assert.equal(await page.locator('.workflow-stage-content .process-output-card').count(),initial.bootstrap.codebook.codes.length);
 passed.push('Real saved run: single workspace, source dialog, codebook search/assignments, all tools, preserved review draft, original bootstrap content');
 await page.locator('.task-toolbar button.primary').click();await page.evaluate(()=>scrollTo(0,0));await page.locator('.workspace-tools > summary').click();await page.screenshot({path:path.join(output,'triggered-review.png')});
 await page.locator('.header-actions button').first().click();await page.locator('.task-form').waitFor();assert(!(await page.locator('.advanced-setup').getAttribute('open')));await page.locator('.advanced-setup summary').click();await page.screenshot({path:path.join(output,'new-task.png')});
 for(const width of [1024,768,390]){await page.setViewportSize({width,height:900});await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(300);const dimensions=await page.evaluate(()=>[innerWidth,document.documentElement.scrollWidth]);if(dimensions[1]>dimensions[0]+1)console.log('OVERFLOW ELEMENTS',await page.locator('body *').evaluateAll(es=>es.map(e=>({tag:e.tagName,cls:e.className,sw:e.scrollWidth,cw:e.clientWidth,display:getComputedStyle(e).display,rect:e.getBoundingClientRect().toJSON()})).filter(e=>e.rect.right>innerWidth+1 || e.sw>e.cw+20).slice(0,30)));assert(dimensions[1]<=dimensions[0]+1,`Overflow at ${width}: ${dimensions}`);}
 await page.screenshot({path:path.join(output,'mobile-new-task.png'),fullPage:true});passed.push('1440 / 1024 / 768 / 390px: no page-level horizontal overflow');
 // Deterministic contract-level UI flow. All writes below are mocked, no agents called.
 const flow=await browser.newPage({viewport:{width:1440,height:1000}});flow.on('pageerror',e=>errors.push(e.message));await flow.addInitScript(()=>localStorage.setItem('coda-language','en'));
 let run=null, state='empty', setting='selective', postCount=0, nextCalls=0;
 let stage=clone(initial);stage.inspection_only=false;stage.review_record=null;stage.context_requests=[];stage.pending_retrospective_tasks=[];stage.completion_issues=[];stage.codebook_editing_allowed=true;
 const makeRun=(status,bootstrap_status='completed')=>({...clone(saved),run_id:'run-ui-contract',status,bootstrap_status,review_setting:setting,review_mode:setting,pending_retrospective_task_count:0,pending_context_request_count:0,awaiting_next_artifact:status==='awaiting_next_artifact',awaiting_context:status==='awaiting_context',initial_review:null,final_review:null});
 await flow.route('**/api/**',async route=>{
  const req=route.request(), p=new URL(req.url()).pathname, method=req.method();let result;
  if(method==='POST')postCount++;
  if(p==='/api/datasets')result=datasets;
  else if(p==='/api/runs'&&method==='GET')result=run?[run]:[];
  else if(p==='/api/runs'&&method==='POST'){const body=req.postDataJSON();assert.equal(body.artifact_limit,12);assert.equal(body.iterative_batch_size,3);run=makeRun('not_started','not_run');state='created';result=run;}
  else if(p.endsWith('/initialize')){run=makeRun('awaiting_initial_review');state='initial';result=run;}
  else if(p.endsWith('/initial-review-setting')){setting=req.postDataJSON().setting;run=makeRun('awaiting_initial_review');result={run,packet:stage};}
  else if(p.endsWith('/stage-reviews/initial')&&method==='POST'){assert.equal(req.postDataJSON().decision,'accept');run=makeRun('in_progress');state='iterative';result={run,review:{}};}
  else if(p.endsWith('/stage-reviews/initial'))result={...stage,inspection_only:new URL(req.url()).searchParams.has('inspection')};
  else if(p.endsWith('/prepare-review')){run=makeRun('awaiting_human_review');state='case';result=packet;}
  else if(p.endsWith('/submit-review')){const body=req.postDataJSON();assert.equal(body.decision,'mark_uncertain');assert(body.pre_read_memo);run=makeRun('awaiting_next_artifact');state='submitted';result={run,codebook};}
  else if(p.endsWith('/next-artifact')){nextCalls++;run=makeRun('awaiting_final_review');state='final';result={run,current:{...current,artifact:null,codebook}};}
  else if(p.endsWith('/stage-reviews/final')&&method==='POST'){run=makeRun('completed');state='complete';result={run,review:{}};}
  else if(p.endsWith('/stage-reviews/final')){result={...clone(final),kind:'final',inspection_only:state==='complete',codebook,context_requests:[],pending_retrospective_tasks:[],completion_issues:[],unresolved_cases:[],codebook_editing_allowed:true,review_scope:{checkpoint:'final',purpose:'Check corpus coverage, assignments, pending decisions and the final codebook.',required_checks:['Coverage and missing materials','Compatibility with the final codebook','Outstanding context and reassessment tasks']},audit_summary:{audit_input_artifacts:16,audit_processed_artifacts:16,pending_retrospective_count:0},final_validation_audits:[]};}
  else if(p.endsWith('/current-artifact'))result={...current,codebook};
  else if(p.endsWith('/codebook'))result=codebook;
  else if(p.includes('/codebook/')&&p.endsWith('/artifacts'))result={code:codebook.codes[0],artifacts:[],artifact_count:0};
  else if(p.endsWith('/history'))result={...history,retrospective_tasks:[],context_requests:[]};
  else if(p.endsWith('/context-requests'))result={requests:[],pending_count:0};
  else if(p.endsWith('/review-packet')){if(state==='case'||state==='submitted')result=packet;else return route.fulfill({status:404,contentType:'application/json',body:JSON.stringify({detail:'No prepared review'})});}
  else if(p.endsWith('/artifacts'))result=artifacts;
  else if(p.endsWith('/review-timer'))result={run};
  else if(p==='/api/runs/run-ui-contract')result=run;
  else throw Error(`Unhandled ${method} ${p}`);
  return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(result)});
 });
 await flow.goto(url);await flow.locator('.task-form').waitFor();await flow.locator('.task-fields > .limit-control input').fill('12');await flow.locator('.advanced-setup summary').click();await flow.locator('.advanced-fields .limit-control input').fill('3');await flow.locator('.task-form button[type=submit]').click();await flow.locator('.task-setup-card').waitFor();assert(await flow.locator('.workflow-sidebar').isVisible());assert.equal(await flow.locator('.new-task-panel').count(),0);
 await flow.locator('.task-setup-card button').click();await flow.locator('.initial-review-setting').waitFor();await flow.locator('.review-setting-option').last().click();await flow.waitForFunction(()=>document.querySelector('.task-policy')?.textContent.includes('Full'));
 await flow.screenshot({path:path.join(output,'initial-review.png')});
 await flow.locator('.stage-review-decision textarea').fill('The category definitions and supporting examples meet the analytical scope.');await flow.locator('.stage-decision-grid button').first().click();await flow.locator('.stage-submit').click();await flow.waitForFunction(()=>document.querySelector('.task-summary')?.textContent.includes('In progress'));
 await flow.locator('.task-actions > button').click();await flow.locator('.review-panel textarea').first().waitFor();await flow.locator('.review-panel textarea').first().fill('The source supports the observed behavior, but the boundary requires human clarification.');await flow.getByRole('button',{name:'Reveal evidence packet',exact:true}).click();await flow.locator('.decision-grid input').nth(3).check();
 const rationale=flow.locator('.review-panel label').filter({has:flow.locator('textarea')}).filter({hasText:/Rationale/i});
 await rationale.locator('textarea').fill('The available evidence does not settle the coding boundary.');await flow.locator('.submit-review').click();await flow.waitForFunction(()=>document.querySelector('.task-summary')?.textContent.includes('Review recorded'));
 await flow.locator('.task-actions > button').click();await flow.locator('.stage-review-decision').waitFor();assert.equal(nextCalls,1);await flow.evaluate(()=>scrollTo(0,0));await flow.screenshot({path:path.join(output,'final-review.png')});await flow.locator('.stage-review-decision textarea').fill('The corpus audit and unresolved register have been checked.');await flow.locator('.stage-decision-grid button').first().click();await flow.locator('.stage-submit').click();await flow.waitForFunction(()=>document.querySelector('.task-summary')?.textContent.includes('Completed'));
 const downloadPromise=flow.waitForEvent('download');await flow.getByRole('button',{name:'Download codebook',exact:true}).click();const dl=await downloadPromise;assert(dl.suggestedFilename().includes('run-ui-contract'));passed.push(`Mocked end-to-end: create + advanced batch size, initialize, select Full Review, initial approval, prepare case, submit unresolved decision, continue, final approval, codebook download (${postCount} POSTs)`);
 // Exercise policy-specific continuation and initialization stop/resume controls.
 for (const policy of ['selective', 'automatic']) {
  setting=policy; state='initial'; run=makeRun('awaiting_initial_review');
  await flow.reload(); await flow.locator('.initial-review-setting').waitFor();
  if (policy==='automatic') {
   await flow.route('**/initial-review-setting', route => {
    assert.equal(route.request().postDataJSON().continue_automatic,true);
    run=makeRun('in_progress');state='iterative';
    return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({run,packet:null})});
   });
   await flow.getByRole('button',{name:'Continue automatically',exact:true}).click();
   await flow.waitForFunction(()=>document.querySelector('.task-summary')?.textContent.includes('In progress'));
   await flow.unroute('**/initial-review-setting');
  } else {
   await flow.locator('.stage-review-decision textarea').fill('Definitions and representative evidence were checked.');
   await flow.locator('.stage-decision-grid button').first().click();await flow.locator('.stage-submit').click();
   await flow.waitForFunction(()=>document.querySelector('.task-summary')?.textContent.includes('In progress'));
  }
  await flow.route('**/process-automatic?*', route => {
   assert.equal(route.request().method(),'POST');
   run=makeRun(policy==='selective'?'awaiting_human_review':'completed');state=policy==='selective'?'case':'complete';
   return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({run,current:{...current,codebook},stopped_for_human:policy==='selective'})});
  });
  await flow.locator('.task-actions > button').click();
  if (policy==='selective') { await flow.locator('.review-panel textarea').first().waitFor();assert(await flow.locator('.execution-phase-node.active').innerText().then(t=>t.includes('Triggered'))); }
  else { await flow.getByRole('button',{name:'Download codebook',exact:true}).waitFor();assert.equal(await flow.locator('.stage-review-decision:visible').count(),0); }
  await flow.unroute('**/process-automatic?*');
 }
 setting='selective';state='created';run=makeRun('not_started','running');
 await flow.route('**/initialize/cancel',route=>{run=makeRun('not_started','cancelled');return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(run)})});
 await flow.reload();await flow.locator('.task-setup-card').waitFor();await flow.locator('.task-actions > button').click();
 await flow.getByRole('button',{name:'Continue initialization',exact:true}).first().waitFor();
 await flow.locator('.task-actions > button').click();await flow.locator('.initial-review-setting').waitFor();
 passed.push('Automatic / Selective policy-specific continuation and initialization pause/resume');
 await flow.locator('.language-select').selectOption('zh');await flow.evaluate(()=>scrollTo(0,0));await flow.screenshot({path:path.join(output,'initial-review-zh.png')});assert((await flow.locator('.task-toolbar').innerText()).includes('选择性审核'));passed.push('Chinese interface labels and initial-review controls');
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);await fs.writeFile(path.join(output,'report.json'),JSON.stringify({passed,errors,failures},null,2));console.log(JSON.stringify({passed,errors,failures},null,2));await browser.close();
}
main().catch(e=>{console.error(e);process.exit(1)});
