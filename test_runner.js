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
    matchMedia: () => ({ matches: false }),
    addEventListener: () => {}
  },
  getComputedStyle: () => ({ paddingLeft: '20px', paddingRight: '20px' }),
  ResizeObserver: class { observe() {} },
  requestAnimationFrame: (fn) => setTimeout(fn, 0),
  localStorage: { getItem: () => null, setItem: () => {} }
};

const context = vm.createContext(sandbox);

// Expose runUnitTests
const modifiedScript = scriptText.replace('init();', 'globalThis.runUnitTests = runUnitTests; init();');
vm.runInContext(modifiedScript, context);

vm.runInContext('runUnitTests();', context);

console.log(testLogElem.textContent);

if (testLogElem.textContent.includes('FAIL:')) {
  console.error('\n❌ Test failures detected!');
  process.exit(1);
} else {
  console.log('\n✨ ALL TESTS PASSED SUCCESSFULLY! ✨');
}
