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
    getContext: () => ({
      fillRect: () => {}, fillText: () => {}, measureText: () => ({ width: 10 }),
      createImageData: (w, h) => ({ data: new Uint8ClampedArray(w * h * 4) }),
      putImageData: () => {}, drawImage: () => {}, save: () => {}, restore: () => {}
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
  'globalThis.runUnitTests = runUnitTests; globalThis.getEquilibria = getEquilibria; globalThis.SYS = SYS; globalThis.initLiveSim = initLiveSim; globalThis.stepLiveSim = stepLiveSim; globalThis.computeJacobian3D = computeJacobian3D; globalThis.classifyJacobian3D = classifyJacobian3D; init();'
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
`, context);

console.log('\n✨ ALL TESTS PASSED SUCCESSFULLY! ✨');
