# Phase Space Prints 🌀🎨

> **Turn differential equations and dynamical systems into high-resolution posters and wallpapers.**

Phase Space Prints is a standalone, self-contained single-page web app built with vanilla HTML5, modern CSS, and JavaScript. It runs entirely in the browser on `<canvas>` using a CPU density buffer with bilinear splatting, custom logarithmic tone mapping, and a hand-written mathematical expression compiler (strictly zero `eval` or `new Function`).

🔗 **Live Web App:** [https://mdsamhussain1996.github.io/phase-space-prints/](https://mdsamhussain1996.github.io/phase-space-prints/) (or open `index.html` locally / serve via `python3 -m http.server 8091`).  
📦 **Repository:** [https://github.com/mdsamhussain1996/phase-space-prints](https://github.com/mdsamhussain1996/phase-space-prints)  
👨‍🏫 **Author:** [Dr. Md Samshad Hussain Ansari](https://mdsamhussain1996.github.io/) (Assistant Professor of Mathematics, ADYPU, Pune)

---

## ✨ Features

### 1. Dynamical Systems Included
- **Strange Attractors (3-D, Fractional-Capable)**:
  - Lorenz ($\sigma=10, \rho=28, \beta=8/3$)
  - Rössler ($a=0.2, b=0.2, c=5.7$)
  - Aizawa ($a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1$)
  - Thomas ($b=0.208186$, cyclic)
  - Halvorsen ($a=1.89$, cyclic)
  - Dadras ($a=3, b=2.7, c=1.7, d=2, e=9$)
  - Chen ($a=35, b=3, c=28$)
- **Fractional-Order Presets**:
  - Solved with the explicit Grünwald–Letnikov scheme (Petráš algorithm) with memory window $L=1000$:
    - Fractional Lorenz ($q=0.995, h=0.005$)
    - Fractional Chen ($q=0.9, h=0.005$)
    - Fractional Rössler ($q=0.9, a=0.5, b=0.2, c=10, h=0.01$)
- **Iterated Maps (2-D)**:
  - Clifford Map ($a=-1.4, b=1.6, c=1, d=0.7$)
  - Peter de Jong Map ($a=1.4, b=-2.3, c=2.4, d=-2.1$)
- **Forced Oscillators**:
  - Ueda–Duffing Oscillator ($\ddot{x} + \delta \dot{x} + \alpha x + \beta x^3 = \gamma \cos \omega t$) sampled once per forcing period (Poincaré section).
- **Phase Portraits**:
  - Van der Pol flow ($G \times G$ grid of trajectories, NaN-separated).
  - Damped pendulum flow.
- **Write Your Own Equations**:
  - Custom equations parser compiling arbitrary 2-D and 3-D ODEs with user constants into closures on a shared `Float64Array`.
  - Default: Nosé–Hoover (Sprott A): $\dot{x} = y, \dot{y} = -x + yz, \dot{z} = a - y^2, a=1, x_0=(0, 5, 0)$.

---

### 2. High-Fidelity Rendering Engine
- **CPU Density Buffer (`Float32Array`)**: Sub-pixel bilinear splatting into 4 neighboring pixels.
- **Logarithmic Tone Mapping**: Based on the 99.5th percentile non-zero density reference level.
- **Two Colouring Modes**:
  - **Density**: Palette LUT indexed by tone-mapped intensity.
  - **Along the path**: Time/jump-blended $R, G, B$ accumulation.
- **8 Curated Color Palettes**: Nebula, Ember, Glacier, Viridis, Copper, Blueprint, Ink on paper, Riso.
- **Interactive 3D Controls**:
  - Turn (yaw) and tilt (pitch) with pointer drag.
  - Fast low-detail preview during drag, full render on release.
  - Optional depth shading and bloom/glow effect.

---

### 3. Print Formats & Gallery Captions
- **Available Print Resolutions**:
  - Square 2048²
  - A3 Poster @ 150 dpi ($1754 \times 2480$)
  - A3 Poster @ 300 dpi ($3508 \times 4961$)
  - Desktop Wallpaper ($2560 \times 1440$)
  - 4K Wallpaper ($3840 \times 2160$)
  - Phone Wallpaper ($1179 \times 2556$)
  - Portrait Post ($1080 \times 1350$)
- **In-Canvas Gallery Caption**: Thin rule, custom display title, initial conditions, monospace equations ($D^q x$ superscripts), and constant readouts.
- **One-Click Recipe**: Copy reproducible parameters with a single button.

---

### 4. Zero `eval` Recursive-Descent Parser
- Grammar: `expr = term { (+|-) term }; term = unary { (*|/|implicit) unary }; unary = (+|-) unary | power; power = primary [^ unary]; primary = number | name | func(args) | (expr)`
- Implicit multiplication (`2x`, `x(ρ - z)`, `a sin(x)`).
- Targeted error messages (e.g. `“xy” is read as one name. Write x*y.`).
- Complete math functions: `sin`, `cos`, `tan`, `exp`, `log`/`ln`, `sqrt`, `abs`, `tanh`, `sinh`, `cosh`, `atan`, `asin`, `acos`, `sign`, `floor`, `min`, `max`, `pow`, `atan2`, `mod`.

---

## 🧪 Unit Tests

Run the built-in test suite in Node.js:
```bash
node test_runner.js
```
Or open the app in a browser and click the **🧪 Test Suite** button in the header. All 16 automated tests verify:
- Operator precedence: $-x^2 = -9$ at $x=3$
- Power right-associativity: $2^{3^2} = 512$
- Implicit products and constants ($\pi, e$)
- Greek constant symbol normalization ($\sigma, \rho$)
- Targeted error messages
- Fractional preset boundedness
- Two-argument functions
- Nosé–Hoover custom ODE compilation
- Mismatched initial state and reserved name validations
- Complete 28-combination format/mode render test matrix
