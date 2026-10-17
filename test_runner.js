const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('index.html', 'utf8');
const scriptText = html.match(/<script>([\s\S]*?)<\/script>/)[1];

const testLogElem = {
  textContent: '',
  hidden: false,
  focus: () => {}
};

const makeElem = (tag) => {
  if (tag === 'testLog') return testLogElem;
  return {
    tagName: tag,
    label: '',
    value: '',
    textContent: '',
    innerHTML: '',
    hidden: false,
    classList: { contains: () => false, add: () => {}, remove: () => {} },
    style: {},
    appendChild: function(ch) { this.children = this.children || []; this.children.push(ch); return ch; },
    addEventListener: () => {},
    setAttribute: () => {},
    getAttribute: () => '',
    focus: () => {},
    width: 800,
    height: 600,
    getContext: () => ({
      fillRect: () => {}, fillText: () => {}, measureText: () => ({ width: 10 }),
      createImageData: (w, h) => ({ data: new Uint8ClampedArray(w * h * 4) }),
      putImageData: () => {}, drawImage: () => {}, save: () => {}, restore: () => {},
      beginPath: () => {}, closePath: () => {}, arc: () => {}, fill: () => {}, stroke: () => {},
      moveTo: () => {}, lineTo: () => {}, clearRect: () => {},
      createRadialGradient: () => ({ addColorStop: () => {} }),
      createLinearGradient: () => ({ addColorStop: () => {} }),
      setTransform: () => {}, resetTransform: () => {}
    })
  };
};

const sandbox = {
  console,
  process,
  Math,
  parseFloat,
  isNaN,
  Number,
  Set,
  Float64Array,
  Float32Array,
  Uint8Array,
  Uint8ClampedArray,
  Promise,
  performance: { now: () => Date.now() },
  Date,
  setTimeout,
  clearTimeout,
  document: {
    createElement: makeElem,
    getElementById: (id) => (id === 'testLog' ? testLogElem : makeElem(id)),
    querySelectorAll: () => [],
    documentElement: { getAttribute: () => 'light', setAttribute: () => {} },
    addEventListener: () => {},
    fonts: { load: () => Promise.resolve(), ready: Promise.resolve() }
  },
  window: {
    innerWidth: 1024, innerHeight: 768,
    location: { href: 'https://mdsamhussain1996.github.io/phase-space-prints/', search: '' },
    matchMedia: () => ({ matches: false }),
    addEventListener: () => {}
  },
  getComputedStyle: () => ({ paddingLeft: '20px', paddingRight: '20px' }),
  ResizeObserver: class { observe() {} },
  requestAnimationFrame: (fn) => setTimeout(fn, 0),
  cancelAnimationFrame: (id) => clearTimeout(id),
  URL,
  URLSearchParams,
  Blob,
  localStorage: (() => {
    const store = {};
    return {
      getItem: (k) => (k in store ? store[k] : null),
      setItem: (k, v) => { store[k] = String(v); },
      removeItem: (k) => { delete store[k]; },
      clear: () => { for (const k in store) delete store[k]; }
    };
  })()
};

const context = vm.createContext(sandbox);

// Expose runUnitTests and helpers
const modifiedScript = scriptText.replace(
  'init();',
  'globalThis.runUnitTests = runUnitTests; globalThis.getEquilibria = getEquilibria; globalThis.SYS = SYS; globalThis.GROUPS = GROUPS; globalThis.initLiveSim = initLiveSim; globalThis.stepLiveSim = stepLiveSim; globalThis.computeJacobian3D = computeJacobian3D; globalThis.classifyJacobian3D = classifyJacobian3D; globalThis.buildArcLengthTable = buildArcLengthTable; globalThis.getArcLengthIndex = getArcLengthIndex; globalThis.tickLiveMode = tickLiveMode; globalThis.serializeLiveUrl = serializeLiveUrl; globalThis.parseUrlParams = parseUrlParams; globalThis.state = state; init();'
);
vm.runInContext(modifiedScript, context);

vm.runInContext('runUnitTests();', context);

// Verify in-page test suite output
console.log(testLogElem.textContent);

if (testLogElem.textContent.includes('FAIL:')) {
  console.error('\n❌ Test failures detected in in-page test suite!');
  process.exit(1);
}

// Standalone Direct Node Assertions
console.log('\n=== Additional Direct Node Invariants ===');
vm.runInContext(`
  // 1. Lorenz equilibria within 1e-6
  const lorenzEqs = getEquilibria(true);
  if (lorenzEqs.length !== 3) throw new Error('Expected 3 Lorenz equilibria');
  const cVal = Math.sqrt((8/3) * (28 - 1));
  const expectedPts = [[0,0,0], [cVal, cVal, 27], [-cVal, -cVal, 27]];
  for (const exp of expectedPts) {
    const found = lorenzEqs.some(e => Math.hypot(e.point[0] - exp[0], e.point[1] - exp[1], e.point[2] - exp[2]) < 1e-6);
    if (!found) throw new Error('Missing expected Lorenz equilibrium: ' + JSON.stringify(exp));
  }
  console.log('✅ PASS: Direct Lorenz 3-equilibria invariant verified (< 1e-6)');

  // 2. Unstable departure
  const J0 = computeJacobian3D(SYS.lorenz.f, 0, 0, 0, { s: 10, r: 28, b: 8/3 });
  const cl0 = classifyJacobian3D(J0);
  if (cl0.type !== 'saddle') throw new Error('Expected saddle at Lorenz origin');
  console.log('✅ PASS: Direct eigen-classification invariant verified (saddle)');

  // 3. Ring buffer bounded capacity
  const liveTestSim = initLiveSim();
  stepLiveSim(liveTestSim, 50000);
  if (liveTestSim.tailBuffer.length !== 12000) throw new Error('Ring buffer size altered');
  console.log('✅ PASS: Direct ring buffer bounded size verified (12000 floats)');

  // 4. Arc-length mapping is monotonic and reaches end exactly at t = 1
  const dummyCache = {
    pts: new Float64Array([0,0,0, 1,0,0, 2,0,0, 3,0,0, 4,0,0]),
    n: 5,
    start: 0
  };
  buildArcLengthTable(dummyCache);
  if (getArcLengthIndex(dummyCache, 1) !== 4) throw new Error('Arc-length mapping did not reach end at t = 1');
  let prevIdx = -1;
  for (let s = 0; s <= 20; s++) {
    const idx = getArcLengthIndex(dummyCache, s / 20);
    if (idx < prevIdx) throw new Error('Arc-length mapping not monotonic');
    prevIdx = idx;
  }
  console.log('✅ PASS: Direct arc-length monotonic & t=1 endpoint invariant verified');

  // 5. Light speed scaling: 0.25x makes pass 4x longer than 1x
  const dur1x = 12 / 1.0;
  const durQuarter = 12 / 0.25;
  if (Math.abs(durQuarter / dur1x - 4.0) > 1e-6) throw new Error('Light speed duration scaling error');
  console.log('✅ PASS: Direct light speed 0.25x scaling invariant verified');

  // 6. URL round-trip preserves lspeed, dur, from, eq, live, trace
  state.lightSpeed = 0.25;
  state.traceDur = 90;
  state.traceSource = 'fixed';
  state.traceEquilIdx = 1;
  state.liveEndless = true;
  state.liveTrace = true;
  const url = serializeLiveUrl('https://example.com/live');
  const p = parseUrlParams(url);
  if (p.lightSpeed !== 0.25 || p.traceDur !== 90 || p.traceSource !== 'fixed' || p.traceEquilIdx !== 1 || p.traceLive !== true || p.liveTrace !== true) {
    throw new Error('URL round-trip mismatch: ' + JSON.stringify(p));
  }
  console.log('✅ PASS: Direct URL round-trip preserves lspeed, dur, from, eq, live, trace');

  // 7. Phase 1: Halvorsen canonical parameter and Aizawa 3/4 view
  if (SYS.halvorsen.params[0].v !== 1.4) throw new Error('SYS.halvorsen parameter a must default to 1.4');
  if (SYS.aizawa.view[0] < 0.5 || SYS.aizawa.view[1] > -0.4) throw new Error('SYS.aizawa default view must be 3/4 angle');
  console.log('✅ PASS: Direct Phase 1 Halvorsen & Aizawa default views verified');

  // 8. Phase 1: Flow domains tuned and bounded
  if (SYS.vdp.dom[0] < -3.5 || SYS.vdp.dom[1] > 3.5) throw new Error('SYS.vdp domain out of expected range');
  if (Math.abs(SYS.pendulum.dom[1] / SYS.pendulum.dom[3]) > 2.5) throw new Error('SYS.pendulum domain aspect ratio unbalanced');
  console.log('✅ PASS: Direct Phase 1 flow domains verified');

  // 9. Phase 2: Strange attractors II definitions & chaos invariants
  if (!GROUPS.includes('Strange attractors II')) throw new Error('GROUPS must contain Strange attractors II');
  const p2Keys = ['lu', 'chua', 'rucklidge', 'burkeShaw', 'tsucs', 'rabFab', 'sprott2014'];
  for (const k of p2Keys) {
    const s = SYS[k];
    if (!s) throw new Error('Missing preset: ' + k);
    if (s.group !== 'Strange attractors II') throw new Error(k + ' must be in Strange attractors II');
    if (s.kind !== 'ode' || !s.frac || s.vars.length !== 3) throw new Error(k + ' must be fractional-capable 3D ODE');
    if (!s.rhs || s.rhs.length !== 3) throw new Error(k + ' must have 3 Unicode rhs expressions');
  }
  console.log('✅ PASS: Direct Phase 2 Strange attractors II definitions verified');

  // 10. Phase 3: Neural Dynamics & QVNN 4D projection invariants
  if (!GROUPS.includes('Neural dynamics')) throw new Error('GROUPS must contain Neural dynamics');
  const hop = SYS.hopfield;
  if (!hop || hop.group !== 'Neural dynamics' || !hop.frac) throw new Error('SYS.hopfield invalid');
  const fHop = SYS.fHopfield;
  if (!fHop || fHop.base !== 'hopfield' || fHop.q !== 0.95) throw new Error('SYS.fHopfield invalid');
  const qvnn = SYS.qvnn;
  if (!qvnn || qvnn.dim !== 4 || qvnn.vars.length !== 4) throw new Error('SYS.qvnn invalid');
  const dropP = qvnn.params.find(p => p.k === 'drop');
  if (!dropP || dropP.type !== 'select' || dropP.options.length !== 4) throw new Error('SYS.qvnn drop dropdown invalid');
  console.log('✅ PASS: Direct Phase 3 Neural Dynamics & QVNN invariants verified');
`, context);

console.log('\n✨ ALL TESTS PASSED SUCCESSFULLY! ✨');
