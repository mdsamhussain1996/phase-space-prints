"""
Phase Space Prints — Mathematical Dynamical Systems Art
Streamlit Edition for Streamlit Community Cloud (streamlit.app)
Author: mdsamhussain1996 (https://mdsamhussain1996.github.io/)
"""
from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.integrate import solve_ivp
import streamlit as st
import streamlit.components.v1 as components

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Phase Space Prints — Mathematical Dynamical Systems Art",
    page_icon="🌀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(120deg, #8b9eff, #ffffff 60%, #e3e7f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #8d95af;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        background: rgba(139, 158, 255, 0.12);
        color: #8b9eff;
        border: 1px solid rgba(139, 158, 255, 0.3);
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .card {
        background: #131724;
        border: 1px solid #262e46;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
    .stat-val {
        font-size: 1.5rem;
        font-weight: 700;
        color: #8b9eff;
    }
    .stat-lbl {
        color: #8d95af;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Sidebar Navigation & Attribution
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
### 🌀 Phase Space Prints
**Generative Dynamical Systems**
""")

view_mode = st.sidebar.radio(
    "Navigation",
    [
        "🎨 Generative Studio (Interactive)",
        "🔬 Python 3D Trajectory Lab",
        "📐 Attractor Equations & Theory",
        "👤 About & Portfolio",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 0.85rem; color: #8d95af;">
Created by <b>mdsamhussain1996</b><br>
🌐 <a href="https://mdsamhussain1996.github.io/" target="_blank" style="color:#8b9eff;">Portfolio Website</a><br>
📂 <a href="https://github.com/mdsamhussain1996/phase-space-prints" target="_blank" style="color:#8b9eff;">GitHub Repository</a><br>
⚡ <a href="https://mdsamhussain1996.github.io/phase-space-prints/" target="_blank" style="color:#8b9eff;">Direct Web App</a>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# View 1: Generative Studio (Interactive Embedded WebGL/Canvas Studio)
# -----------------------------------------------------------------------------
if view_mode == "🎨 Generative Studio (Interactive)":
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.markdown('<div class="main-title">Phase Space Prints Studio</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="subtitle">Interactive phase-portrait generator with 3D rotation, sub-pixel density accumulation, logarithmic tone-mapping, and gallery print export.</div>',
            unsafe_allow_html=True,
        )
    with col_t2:
        st.markdown(
            """
            <div style="text-align: right; padding-top: 10px;">
                <a href="https://mdsamhussain1996.github.io/phase-space-prints/" target="_blank" style="
                    display: inline-block;
                    padding: 8px 16px;
                    border-radius: 8px;
                    background: #2b45c7;
                    color: #ffffff;
                    text-decoration: none;
                    font-weight: 600;
                    font-size: 0.9rem;">Open Fullscreen ↗</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Read and embed the complete self-contained index.html
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        html_code = html_path.read_text(encoding="utf-8")
        components.html(html_code, height=920, scrolling=True)
    else:
        st.error("index.html not found in project directory.")


# -----------------------------------------------------------------------------
# View 2: Python 3D Trajectory Lab (Numerical SciPy Simulator & Data Exporter)
# -----------------------------------------------------------------------------
elif view_mode == "🔬 Python 3D Trajectory Lab":
    st.markdown('<div class="main-title">Python 3D Trajectory Lab</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Compute high-precision phase-space paths using SciPy RK45 integration, analyze velocity distributions, and export trajectory coordinates.</div>',
        unsafe_allow_html=True,
    )

    SYSTEMS = {
        "Lorenz Attractor": {
            "func": lambda t, s, p: [
                p["sigma"] * (s[1] - s[0]),
                s[0] * (p["rho"] - s[2]) - s[1],
                s[0] * s[1] - p["beta"] * s[2],
            ],
            "default_params": {"sigma": 10.0, "rho": 28.0, "beta": 8.0 / 3.0},
            "default_init": [0.1, 1.0, 1.0],
            "t_span": (0, 40),
            "max_step": 0.01,
            "desc": "Classical weather convection model with butterfly manifold.",
        },
        "Aizawa Attractor": {
            "func": lambda t, s, p: [
                (s[2] - p["b"]) * s[0] - p["d"] * s[1],
                p["d"] * s[0] + (s[2] - p["b"]) * s[1],
                p["c"] + p["a"] * s[2] - (s[2] ** 3) / 3.0 - (s[0] ** 2 + s[1] ** 2) * (1.0 + p["e"] * s[2]) + p["f"] * s[2] * (s[0] ** 3),
            ],
            "default_params": {"a": 0.95, "b": 0.7, "c": 0.6, "d": 3.5, "e": 0.25, "f": 0.1},
            "default_init": [0.1, 0.0, 0.0],
            "t_span": (0, 60),
            "max_step": 0.015,
            "desc": "Spherical chaotic flow with polar tube circulation.",
        },
        "Chen Attractor": {
            "func": lambda t, s, p: [
                p["a"] * (s[1] - s[0]),
                (p["c"] - p["a"]) * s[0] - s[0] * s[2] + p["c"] * s[1],
                s[0] * s[1] - p["b"] * s[2],
            ],
            "default_params": {"a": 35.0, "b": 3.0, "c": 28.0},
            "default_init": [-0.1, 0.5, -0.6],
            "t_span": (0, 35),
            "max_step": 0.01,
            "desc": "Dual-scroll attractor satisfying the topological Shilnikov criteria.",
        },
        "Thomas Attractor": {
            "func": lambda t, s, p: [
                np.sin(s[1]) - p["b"] * s[0],
                np.sin(s[2]) - p["b"] * s[1],
                np.sin(s[0]) - p["b"] * s[2],
            ],
            "default_params": {"b": 0.208186},
            "default_init": [1.1, 1.1, -0.1],
            "t_span": (0, 150),
            "max_step": 0.05,
            "desc": "Cyclic, highly labyrinthine 3D chaotic attractor.",
        },
        "Halvorsen Attractor": {
            "func": lambda t, s, p: [
                -p["a"] * s[0] - 4 * s[1] - 4 * s[2] - s[1] ** 2,
                -p["a"] * s[1] - 4 * s[2] - 4 * s[0] - s[2] ** 2,
                -p["a"] * s[2] - 4 * s[0] - 4 * s[1] - s[0] ** 2,
            ],
            "default_params": {"a": 1.89},
            "default_init": [-1.48, -1.5, 0.0],
            "t_span": (0, 60),
            "max_step": 0.02,
            "desc": "Cyclic 3-fold symmetric strange attractor.",
        },
        "Rössler Attractor": {
            "func": lambda t, s, p: [
                -s[1] - s[2],
                s[0] + p["a"] * s[1],
                p["b"] + s[2] * (s[0] - p["c"]),
            ],
            "default_params": {"a": 0.2, "b": 0.2, "c": 5.7},
            "default_init": [1.0, 1.0, 1.0],
            "t_span": (0, 100),
            "max_step": 0.02,
            "desc": "Single-spiral chaotic attractor with a Möbius strip topology.",
        },
        "Dadras Attractor": {
            "func": lambda t, s, p: [
                s[1] - p["a"] * s[0] + p["b"] * s[1] * s[2],
                p["c"] * s[1] - s[0] * s[2] + s[2],
                p["d"] * s[2] - p["e"] - s[0] * s[1],
            ],
            "default_params": {"a": 3.0, "b": 2.7, "c": 1.7, "d": 2.0, "e": 9.0},
            "default_init": [1.1, 2.1, -0.1],
            "t_span": (0, 40),
            "max_step": 0.01,
            "desc": "Multiscroll 5-parameter chaotic flow.",
        },
    }

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("### ⚙️ Simulation Parameters")
        selected_system = st.selectbox("Select Attractor", list(SYSTEMS.keys()), index=0)
        sys_info = SYSTEMS[selected_system]
        st.info(sys_info["desc"])

        params = {}
        for p_name, p_val in sys_info["default_params"].items():
            params[p_name] = st.number_input(
                f"Parameter: {p_name}",
                value=float(p_val),
                format="%.5f" if isinstance(p_val, float) else "%f",
            )

        st.markdown("**Initial State $(x_0, y_0, z_0)$**")
        ci1, ci2, ci3 = st.columns(3)
        init_x = ci1.number_input("x₀", value=sys_info["default_init"][0])
        init_y = ci2.number_input("y₀", value=sys_info["default_init"][1])
        init_z = ci3.number_input("z₀", value=sys_info["default_init"][2])
        init_state = [init_x, init_y, init_z]

        st.markdown("**Integration Settings**")
        t_max = st.slider("Time Span ($t_{\\max}$)", 10, 200, sys_info["t_span"][1])
        color_scheme = st.selectbox(
            "Plotly Color Scheme",
            ["Plasma", "Viridis", "Turbo", "Magma", "Inferno", "Cividis", "Electric"],
            index=0,
        )

    with c2:
        st.markdown("### 📊 Interactive 3D Phase Space Trajectory")
        with st.spinner("Computing numerical integration via solve_ivp (RK45)..."):
            sol = solve_ivp(
                fun=lambda t, s: sys_info["func"](t, s, params),
                t_span=(0, t_max),
                y0=init_state,
                method="RK45",
                max_step=sys_info["max_step"],
                dense_output=True,
            )

            t_eval = np.linspace(0, t_max, len(sol.t))
            xs, ys, zs = sol.y[0], sol.y[1], sol.y[2]

            # Calculate instantaneous speed for coloring
            vx = np.gradient(xs, t_eval)
            vy = np.gradient(ys, t_eval)
            vz = np.gradient(zs, t_eval)
            speed = np.sqrt(vx**2 + vy**2 + vz**2)

            # Build 3D Scatter plot
            fig = go.Figure(
                data=[
                    go.Scatter3d(
                        x=xs,
                        y=ys,
                        z=zs,
                        mode="lines",
                        line=dict(
                            color=speed,
                            colorscale=color_scheme,
                            width=2.5,
                            colorbar=dict(title="Velocity |v|", len=0.6, thickness=12),
                        ),
                        hoverinfo="text",
                        text=[f"t={t:.2f}s | (x:{x:.2f}, y:{y:.2f}, z:{z:.2f})" for t, x, y, z in zip(t_eval, xs, ys, zs)],
                    )
                ]
            )

            fig.update_layout(
                scene=dict(
                    xaxis=dict(backgroundcolor="#0b0e17", gridcolor="#262e46", showbackground=True),
                    yaxis=dict(backgroundcolor="#0b0e17", gridcolor="#262e46", showbackground=True),
                    zaxis=dict(backgroundcolor="#0b0e17", gridcolor="#262e46", showbackground=True),
                    aspectmode="cube",
                ),
                margin=dict(l=0, r=0, b=0, t=0),
                paper_bgcolor="#0b0e17",
                height=620,
            )

            st.plotly_chart(fig, use_container_width=True)

    # Metrics Summary
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Integrator Steps", f"{len(xs):,}")
    m2.metric("Bounding Box (x)", f"[{xs.min():.1f}, {xs.max():.1f}]")
    m3.metric("Bounding Box (y)", f"[{ys.min():.1f}, {ys.max():.1f}]")
    m4.metric("Mean Velocity", f"{np.mean(speed):.2f}")

    # Data Export Options
    st.markdown("### 💾 Export Trajectory Data")
    df = pd.DataFrame({"t": t_eval, "x": xs, "y": ys, "z": zs, "vx": vx, "vy": vy, "vz": vz, "speed": speed})

    ed1, ed2 = st.columns(2)
    csv_buf = df.to_csv(index=False).encode("utf-8")
    ed1.download_button(
        label="⬇️ Download Trajectory CSV",
        data=csv_buf,
        file_name=f"{selected_system.lower().replace(' ', '_')}_trajectory.csv",
        mime="text/csv",
    )

    npy_buf = io.BytesIO()
    np.save(npy_buf, sol.y.T)
    ed2.download_button(
        label="⬇️ Download NumPy Matrix (.npy)",
        data=npy_buf.getvalue(),
        file_name=f"{selected_system.lower().replace(' ', '_')}_coords.npy",
        mime="application/octet-stream",
    )


# -----------------------------------------------------------------------------
# View 3: Attractor Equations & Theory
# -----------------------------------------------------------------------------
elif view_mode == "📐 Attractor Equations & Theory":
    st.markdown('<div class="main-title">Mathematical Theory & Equations</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Complete formulation of continuous chaotic systems, fractional-order dynamical schemes, and discrete iterated maps.</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Classical Attractors (ODE)", "Fractional-Order Systems", "Iterated Maps"])

    with tab1:
        st.markdown("### 1. Lorenz Attractor (1963)")
        st.latex(r"""
        \begin{cases}
        \dot{x} = \sigma (y - x) \\
        \dot{y} = x (\rho - z) - y \\
        \dot{z} = x y - \beta z
        \end{cases}
        """)
        st.markdown(
            "Derived by Edward Lorenz as a reduced 3-mode model of Rayleigh-Bénard atmospheric convection. "
            "For standard parameters $\\sigma = 10$, $\\rho = 28$, $\\beta = 8/3$, the system exhibits deterministic chaos with a fractional Lyapunov dimension $D_L \\approx 2.06$."
        )

        st.markdown("---")
        st.markdown("### 2. Aizawa Attractor")
        st.latex(r"""
        \begin{cases}
        \dot{x} = (z - b) x - d y \\
        \dot{y} = d x + (z - b) y \\
        \dot{z} = c + a z - \frac{z^3}{3} - (x^2 + y^2)(1 + e z) + f z x^3
        \end{cases}
        """)
        st.markdown(
            "Constructed by Yoji Aizawa. Features a circulating torus that flares outward into chaotic bursts along the $z$-axis."
        )

        st.markdown("---")
        st.markdown("### 3. Chen Attractor")
        st.latex(r"""
        \begin{cases}
        \dot{x} = a (y - x) \\
        \dot{y} = (c - a) x - x z + c y \\
        \dot{z} = x y - b z
        \end{cases}
        """)
        st.markdown(
            "Discovered by Guanrong Chen in 1999 as the dual companion to the Lorenz attractor satisfying the condition $a_{12} a_{21} > 0$."
        )

        st.markdown("---")
        st.markdown("### 4. Thomas Cyclically Symmetric Attractor")
        st.latex(r"""
        \begin{cases}
        \dot{x} = \sin(y) - b x \\
        \dot{y} = \sin(z) - b y \\
        \dot{z} = \sin(x) - b z
        \end{cases}
        """)
        st.markdown("Features 3-fold cyclic symmetry and labyrinthine phase trajectories through periodic potential wells.")

    with tab2:
        st.markdown("### Fractional Calculus & Grünwald–Letnikov Scheme")
        st.markdown(
            """
            In fractional-order dynamical systems, the integer derivative operator $\\frac{d}{dt}$ is replaced with the fractional operator $D^q_t$ for $0 < q \\le 1$.
            The **Grünwald–Letnikov definition** discretizes the non-local memory kernel:
            """
        )
        st.latex(r"""
        D^q_t x(t) = \lim_{h \to 0} \frac{1}{h^q} \sum_{k=0}^{\lfloor (t-t_0)/h \rfloor} (-1)^k \binom{q}{k} x(t - k h)
        """)
        st.markdown(
            """
            Using Petráš' algorithm with memory window $L = 1000$:
            """
        )
        st.latex(r"""
        x(t_k) = f(x(t_{k-1})) h^q - \sum_{j=1}^{L} c_j^{(q)} x(t_{k-j}), \quad c_j^{(q)} = \left(1 - \frac{1 + q}{j}\right) c_{j-1}^{(q)}, \quad c_0^{(q)} = 1
        """)
        st.markdown("Fractional systems capture anomalous dissipation and viscoelastic relaxation found in real-world physical and neural networks.")

    with tab3:
        st.markdown("### Iterated 2-D Chaotic Maps")
        st.markdown("#### Clifford Map")
        st.latex(r"""
        \begin{cases}
        x_{n+1} = \sin(a y_n) + c \cos(a x_n) \\
        y_{n+1} = \sin(b x_n) + d \cos(b y_n)
        \end{cases}
        """)
        st.markdown("#### Peter de Jong Map")
        st.latex(r"""
        \begin{cases}
        x_{n+1} = \sin(a y_n) - \cos(b x_n) \\
        y_{n+1} = \sin(c x_n) - \cos(d y_n)
        \end{cases}
        """)


# -----------------------------------------------------------------------------
# View 4: About & Portfolio
# -----------------------------------------------------------------------------
elif view_mode == "👤 About & Portfolio":
    st.markdown('<div class="main-title">About the Creator & Project</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="card">
            <h3>🌐 Author Portfolio & Research</h3>
            <p>Built by <b>mdsamhussain1996</b>. Specializing in computational mathematics, fractional-order dynamical systems, neural synchronization, and generative scientific visualization.</p>
            <p>
                👉 <b>Visit Portfolio</b>: <a href="https://mdsamhussain1996.github.io/" target="_blank" style="color:#8b9eff; font-weight:700;">https://mdsamhussain1996.github.io/</a><br>
                👉 <b>GitHub Project</b>: <a href="https://github.com/mdsamhussain1996/phase-space-prints" target="_blank" style="color:#8b9eff; font-weight:700;">https://github.com/mdsamhussain1996/phase-space-prints</a><br>
                👉 <b>Live Web App (GitHub Pages)</b>: <a href="https://mdsamhussain1996.github.io/phase-space-prints/" target="_blank" style="color:#8b9eff; font-weight:700;">https://mdsamhussain1996.github.io/phase-space-prints/</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
    ### 🚀 Deploying on Streamlit Community Cloud (`streamlit.app`)
    This repository is now fully structured to be deployed in 1-click on Streamlit Cloud:
    1. Go to [share.streamlit.io](https://share.streamlit.io/)
    2. Click **New app**
    3. Select Repository: `mdsamhussain1996/phase-space-prints`
    4. Select Main file path: `streamlit_app.py`
    5. Click **Deploy!**
    """)
