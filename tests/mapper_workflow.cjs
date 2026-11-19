/* Real browser journey. No intercepted application requests or mocked saves.
 * Usage: NODE_PATH=<playwright modules> node tests/mapper_workflow.cjs <state.json> <artifacts>
 * Refuses to mutate any server without the disposable fixture's nonce header.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const {chromium} = require('playwright');

async function run() {
  const state = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  if (process.argv[4]) state.root = path.resolve(process.argv[4]);
  const out = path.resolve(process.argv[3]);
  fs.mkdirSync(out, {recursive:true});
  const browser = await chromium.launch({headless:true,
    ...(process.env.PLAYWRIGHT_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_EXECUTABLE_PATH} : {})});
  const contexts = [];
  const checks = [], errors = [], serverErrors = [];
  const base = state.base_url;
  const context = async () => {
    const ctx = await browser.newContext({baseURL:base, viewport:{width:1440,height:1000}});
    ctx.setDefaultTimeout(15000);
    contexts.push(ctx);
    ctx.on('page', page => {
      page.on('dialog', dialog => dialog.accept());
      page.on('pageerror', error => errors.push(error.message));
      page.on('response', response => {
        if (response.url().startsWith(base) && response.status() >= 500)
          serverErrors.push(response.status() + ' ' + response.url());
      });
    });
    return ctx;
  };
  const check = (name, ok=true) => { assert.ok(ok, name); checks.push(name); };
  const login = async (page, username, password) => {
    const response = await page.goto(base + '/admin/login');
    assert.equal(response.headers()['x-edrefcard-test-instance'], state.nonce,
      'Refusing to write to a non-fixture server');
    await page.locator('#username').fill(username);
    await page.locator('#password').fill(password);
    await Promise.all([page.waitForURL(url => !url.pathname.endsWith('/login')),
      page.getByRole('button', {name:'Sign in',exact:true}).click()]);
  };
  const save = async page => {
    const result = page.waitForResponse(r => r.url().endsWith('/mapping-editor/save') && r.request().method()==='POST');
    await page.locator('#btnsave').click();
    const response = await result;
    assert.equal(response.status(), 200, await response.text());
    await page.waitForFunction(() => !saveInFlight);
    return response.json();
  };
  const rowFor = page => page.locator('tr').filter({has:page.locator('code', {hasText:'TEST0001'})});
  const imageHash = async page => {
    await page.goto(base + '/binds/ci-profile');
    const img = page.locator('img.refcard-image[alt="Controller Reference Card"]');
    await img.waitFor();
    const response = await page.request.get(await img.getAttribute('src'));
    assert.equal(response.status(), 200);
    return crypto.createHash('sha256').update(await response.body()).digest('hex');
  };
  let admin, mapper, publicPage;
  try {
    const adminCtx = await context(), mapperCtx = await context(), publicCtx = await context();
    admin = await adminCtx.newPage();
    mapper = await mapperCtx.newPage();
    publicPage = await publicCtx.newPage();
    // Verify the nonce before the first state-changing request.
    await login(admin,'ci-admin',state.admin_password);
    check('Session admin login');
    await admin.goto(base + '/admin/users');
    const form = admin.locator('form[action$="/users/create"]');
    await form.locator('[name=username]').fill('ci-mapper');
    await form.locator('[name=password]').fill(state.mapper_password);
    await form.locator('[name=role]').selectOption('mapper');
    await Promise.all([admin.waitForURL(base + '/admin/users'), form.locator('button[type=submit]').click()]);
    await login(mapper,'ci-mapper',state.mapper_password);
    check('Admin creates a mapper and mapper session login succeeds');
    check('Mapper cannot access user administration', (await mapper.request.get(base + '/admin/users')).status()===403);
    check('Mapper cannot publish', (await mapper.request.post(base + '/admin/controllers/publish', {
      headers:{Origin:base}, form:{mapping_id:'1', state:'published'}})).status()===403);

    await mapper.goto(base + '/admin/mapping-editor');
    assert.equal(await mapper.title(),'Mapping editor - EDRefCard admin');
    await mapper.locator('#deviceid').fill('TEST0001');
    await mapper.locator('#title').fill('CI original');
    await mapper.locator('#pad').uncheck();
    await mapper.locator('#file').setInputFiles(path.join(state.root,'original.png'));
    const upload = mapper.waitForResponse(r => r.url().endsWith('/mapping-editor/upload'));
    await mapper.locator('#btnupload').click();
    assert.equal((await upload).status(),200);
    await mapper.waitForFunction(() => !saveInFlight && state.image && scale > 0);
    await mapper.locator('#scaffolder').evaluate(el => {el.open=true;});
    await mapper.locator('#sc_btn').fill('1');
    await mapper.locator('#sc_pov').fill('0');
    await mapper.locator('.sc_ax[value=X]').uncheck();
    await mapper.locator('#btnscaffold').click();
    check('Photo upload and blank scaffold create two real input groups',
      await mapper.locator('.boxcard').count()===2);
    const photo = await mapper.locator('#img').boundingBox();
    assert.ok(photo && photo.width > 0);
    for (let index=0; index<2; index++) {
      await mapper.locator(`[data-setbtn="${index}"]`).click();
      await mapper.locator('#stage').click({position:{x:photo.width*.52,y:photo.height*(.4+index*.15)}});
    }
    check('Physical anchors are placed through the editor', await mapper.locator('.marker').count()===2);
    await mapper.locator('#previewreference').fill('ci-profile');
    await mapper.locator('#btnpreview').click();
    await mapper.locator('#previewcoverage').filter({hasText:'All bound inputs are covered'}).waitFor();
    check('Real bind preview covers both assigned inputs');
    const brokenPreview = {...await mapper.evaluate(() => mapping()), image:'ci-missing-image'};
    const failedPreview = await mapper.request.post(base + '/admin/mapping-editor/preview', {
      headers:{Origin:base}, data:{mapping:brokenPreview}});
    assert.equal(failedPreview.status(),500);
    assert.match((await failedPreview.json()).error, /Preview failed/);
    check('Unexpected rendering failure returns a structured error instead of crashing its logger');
    const first = await save(mapper);
    check('Mapper saves a non-public draft', first.public_status==='draft');
    await mapper.reload();
    assert.equal(await mapper.locator('#title').inputValue(),'CI original');
    check('Saved draft reopens with the original title');
    await publicPage.goto(base + '/binds/ci-profile');
    check('Draft does not render publicly', await publicPage.locator('img.refcard-image').count()===0);

    await admin.goto(base + '/admin/controllers');
    await rowFor(admin).getByRole('button',{name:'Publish',exact:true}).click();
    await admin.waitForLoadState('load');
    const publishedOne = await imageHash(publicPage);
    check('Admin publication makes the card render publicly');
    await mapper.reload();
    const stale = await mapperCtx.newPage();
    await stale.goto(base + '/admin/mapping-editor?device=TEST0001');
    await mapper.locator('#title').fill('CI recovered draft');
    await mapper.waitForFunction(() => Object.keys(localStorage).some(k =>
      k.startsWith('mapedit:') && localStorage.getItem(k).includes('CI recovered draft')));
    await mapper.reload();
    await mapper.locator('#btnrestore').click();
    assert.equal(await mapper.locator('#title').inputValue(),'CI recovered draft');
    check('Unsaved work survives reload and restores through the UI');

    await mapper.locator('#file').setInputFiles(path.join(state.root,'replacement.png'));
    await mapper.locator('#btnupload').click();
    await mapper.waitForFunction(() => !saveInFlight);
    await save(mapper);
    check('Draft title and replacement photo leave the public image byte-identical',
      await imageHash(publicPage)===publishedOne);
    await stale.locator('#title').fill('CI stale tab');
    const conflict = stale.waitForResponse(r => r.url().endsWith('/mapping-editor/save'));
    await stale.locator('#btnsave').click();
    assert.equal((await conflict).status(),409);
    await stale.waitForFunction(() => !saveInFlight);
    check('A stale real tab receives 409 and preserves its unsaved work',
      await stale.evaluate(() => dirty && $('#title').value==='CI stale tab' && !!localStorage.getItem(LS_KEY)));
    await stale.close();

    await admin.goto(base + '/admin/controllers');
    await rowFor(admin).getByRole('button',{name:'Publish draft',exact:true}).click();
    await admin.waitForLoadState('load');
    const publishedTwo = await imageHash(publicPage);
    check('Publishing the reviewed draft changes the public card', publishedTwo!==publishedOne);
    for (const format of ['A4','Letter']) {
      const pdf = await publicPage.request.get(base + '/download/ci-profile/pdf?format=' + format);
      assert.equal(pdf.status(),200);
      assert.equal((await pdf.body()).subarray(0,5).toString(),'%PDF-');
      fs.writeFileSync(path.join(out,format+'.pdf'),await pdf.body());
    }
    check('Published card exports real A4 and Letter PDFs');
    await admin.goto(base + '/admin/controllers/history/' + first.id);
    const versionRows = admin.locator('tbody tr');
    const oldest = versionRows.last();
    const originalVersion = await admin.request.get(await oldest.getByRole('link',{name:'JSON',exact:true}).getAttribute('href'));
    assert.equal((await originalVersion.json()).title,'CI original');
    await oldest.getByRole('button',{name:'Rollback to draft',exact:true}).click();
    await admin.waitForLoadState('load');
    check('Rollback appends a new history version', await admin.locator('tbody tr').count()===3);
    check('Rollback leaves the current public card byte-identical', await imageHash(publicPage)===publishedTwo);
    await mapper.goto(base + '/admin/mapping-editor?device=TEST0001');
    if (await mapper.locator('#btndiscardlocal').isVisible()) await mapper.locator('#btndiscardlocal').click();
    assert.equal(await mapper.locator('#title').inputValue(),'CI original');
    check('Restored version reopens as a draft');
    await admin.goto(base + '/admin/controllers');
    await rowFor(admin).getByRole('button',{name:'Publish draft',exact:true}).click();
    await admin.waitForLoadState('load');
    check('Explicit publication of rollback restores the original public card', await imageHash(publicPage)===publishedOne);
    await publicPage.goto(base + '/');
    await publicPage.locator('#fileupload').setInputFiles(path.join(state.root,'ci-upload.binds'));
    await publicPage.locator('[name=public]').uncheck();
    await publicPage.getByRole('button',{name:/^Generate/}).click();
    await publicPage.locator('img.refcard-image[alt="Controller Reference Card"]').waitFor();
    check('Fresh .binds upload renders the published controller');
    await publicPage.reload();
    await publicPage.locator('img.refcard-image[alt="Controller Reference Card"]').waitFor();
    check('Uploaded card reopens successfully');
    const api = await publicPage.request.post(base + '/api/v1/generate', {multipart:{
      bindings:{name:'ci-api.binds',mimeType:'application/xml',
        buffer:fs.readFileSync(path.join(state.root,'ci-upload.binds'))},
      public:'off', styling:'group'}});
    assert.equal(api.status(),200,await api.text());
    const generated = await api.json();
    assert.equal(generated.status,'success');
    assert.equal(generated.images_created.length,1);
    assert.deepEqual(generated.unsupported_devices,[]);
    await publicPage.goto(generated.url);
    await publicPage.locator('img.refcard-image[alt="Controller Reference Card"]').waitFor();
    check('API generation and saved-card reopening use the same published controller');
    check('No browser JavaScript errors', errors.length===0);
    check('No unexpected page HTTP 5xx responses', serverErrors.length===0);
    await admin.screenshot({path:path.join(out,'controllers.png'),fullPage:false});
    await mapper.screenshot({path:path.join(out,'editor.png'),fullPage:false});
    await publicPage.screenshot({path:path.join(out,'public-card.png'),fullPage:false});
    fs.writeFileSync(path.join(out,'checks.json'),JSON.stringify({checks,errors,serverErrors},null,2));
    console.log(JSON.stringify({passed:checks.length,checks}));
  } catch (error) {
    for (const [name,page] of [['admin',admin],['mapper',mapper],['public',publicPage]])
      if (page && !page.isClosed()) await page.screenshot({path:path.join(out,name+'-failure.png'),fullPage:false}).catch(()=>{});
    fs.writeFileSync(path.join(out,'failure.json'),JSON.stringify({checks,errors,serverErrors,error:String(error)},null,2));
    throw error;
  } finally {
    for (const ctx of contexts) await ctx.close();
    await browser.close();
  }
}
run().catch(error => { console.error(error); process.exitCode=1; });
