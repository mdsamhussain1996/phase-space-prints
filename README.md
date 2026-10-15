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

### 4. ✨ "Light from the Source" Glow Animation
- **Light Source Selection**:
  - **Initial point $x_0$** (default orbit departure).
  - **Fixed point (equilibrium)**: Trajectory is born at an equilibrium $x^*$ and departs along its unstable manifold $x^* + \varepsilon v$ ($\varepsilon \approx 10^{-4} \cdot \text{scale}$). If the chosen point is stable, starts with a gentle kick.
  - **Equilibria Solver**:
    - Continuous 3D ODEs & custom models: Solves $f(x)=0$ with damped Newton's method using a finite-difference Jacobian, seeded from $x_0$, the origin, analytic formulas (Lorenz & Chen), and random points across the attractor's bounding box.
    - 2-D maps: Fixed points of $F(x) - x = 0$ via 2D Newton.
    - Closed-form 3×3 cubic characteristic polynomial solver (Cardano/Viète) classifying equilibria as *saddle*, *saddle-focus*, *unstable focus*, *unstable node*, *stable node*, or *stable focus*.
  - **Pulsing Source Indicator**: Concentric pulsing marker ring drawn at the chosen source point.
- **Luminous Comet Glow Quality**:
  - **Bloom Head**: Radial-gradient bloom with near-white core (`#ffffff`) and halo in the palette's brightest LUT colour, with organic micro-flicker.
  - **Additive Blending Tail**: Exponential decay $\alpha(s) = \exp(-3.5(1-s))$ and width tapering with additive/multiply blending.
  - **Burn-In Density Buffer**: Past trail deposits into the canvas buffer so that at $100\%$ progress the canvas seamlessly equals the static print (pixel diff = 0).
  - **Hold Glow at End Point**: Optional toggle keeps the glowing head at the final state.
  - **Mid-Animation Dragging**: Dragging to rotate (yaw/pitch) or zoom updates the projection smoothly in real time.

---

### 5. 🔴 Live Mode & Wallpaper Integration
- **Endless Live Mode**:
  - Integrates on the fly (RK4, Grünwald–Letnikov fractional, discrete map iterations) at user-configured speed (100–4000 steps/sec).
  - **Dissipative Trail Decay**: Trail decay slider ($0$ to $0.10$) gently dissipates older density so the attractor "breathes" without saturating.
  - **Bounded Memory Safety**: Tail uses a fixed $4000 \times 3$ circular ring buffer ($O(1)$ memory). Fractional GL history stays strictly capped at $L=1000$.
  - **Divergence Detection**: Gracefully detects unbounded escape ($|x| + |y| + |z| > 10^6$), prompts with a warning, and offers restart from source.
  - **Background Pause**: Automatically pauses when the browser tab is hidden (`visibilitychange`) and resumes upon return.
- **A. Full-Screen Ambient Live Wallpaper**:
  - Fullscreen display with Screen Wake Lock (`navigator.wakeLock`).
  - Auto-rotation with pitch wobble and breathing exposure.
  - **Shareable Live URL**: Restores entire configuration from query parameters:
    `?sys=lorenz&live=1&from=fixed&eq=1&speed=800&decay=0.02&holdend=1&palette=nebula&mode=path&yaw=30&pitch=-20&zoom=1.1`
- **B. Looping Video Export**:
  - Records live or precomputed animations in Phone ($1080 \times 2340$), Desktop ($1920 \times 1080$), or Square ($1080 \times 1080$) at 30 fps via `MediaRecorder` (H.264 MP4 / WebM).

---

### 6. Zero `eval` Recursive-Descent Parser
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
Or open the app in a browser and click the **🧪 Test Suite** button in the header. All 57 automated unit tests verify:
- Operator precedence: $-x^2 = -9$ at $x=3$
- Power right-associativity: $2^{3^2} = 512$
- Implicit products and constants ($\pi, e$)
- Greek constant symbol normalization ($\sigma, \rho$)
- Targeted error messages and unbalanced brackets
- Fractional preset boundedness
- Two-argument functions
- Nosé–Hoover custom ODE compilation
- Mismatched initial state and reserved name validations
- Complete 28-combination format/mode render test matrix
- View projection & deterministic rendering
- Lorenz equilibria found by Newton matching analytic three points within $10^{-6}$
- 3×3 Eigen-classification: Lorenz origin classified as saddle; Clifford & De Jong fixed points $|F(x^*) - x^*| < 10^{-9}$
- Unstable manifold departure distance growth over 200 RK4 steps
- Live mode circular ring buffer invariance ($12000$ floats after 100k steps) & fractional GL memory cap $\le L$
- Full URL parameter round-trip with `from`, `eq`, `speed`, `decay`, `holdend`, `live`
- Final frame of non-live trace matching static print render (diff = 0)
- Operator precedence: $-x^2 = -9$ at $x=3$
- Power right-associativity: $2^{3^2} = 512$
- Implicit products and constants ($\pi, e$)
- Greek constant symbol normalization ($\sigma, \rho$)
- Targeted error messages and unbalanced brackets
- Fractional preset boundedness
- Two-argument functions
- Nosé–Hoover custom ODE compilation
- Mismatched initial state and reserved name validations
- Complete 28-combination format/mode render test matrix
- `buildView()` view projection and deterministic pixel rendering
- Trace progress easing and start/end point mapping
- Shareable live wallpaper URL parameter serialization round-trip
- `MediaRecorder` MIME selection and fallback
- Persistent `state` serialization and retrieval for all trace and live parameters

## 🚀 Streamlit Cloud Deployment (`streamlit.app`)

You can run this project as a **Streamlit Web Application** locally or on **[Streamlit Community Cloud](https://share.streamlit.io/)**:

### Run Locally:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Deploy to Streamlit Community Cloud:
1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Connect your GitHub account and click **New app**
3. Set **Repository**: `mdsamhussain1996/phase-space-prints`
4. Set **Branch**: `main`
5. Set **Main file path**: `streamlit_app.py` (or `app.py`)
6. Click **Deploy!**

---

## 👤 Author & Portfolio
Created by [mdsamhussain1996](https://mdsamhussain1996.github.io/) — visit my [Portfolio](https://mdsamhussain1996.github.io/) for more interactive maths, scientific machine learning, and AI projects.
