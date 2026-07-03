#!/usr/bin/env python3
"""Tetracoil magnetic field-line visualisation (self-contained).

Author: Adil Wahab Bhatti
Requires only numpy and matplotlib.

Draws exact field lines of the tetracoil (Gottardi et al. 2003): for an
axisymmetric system, field lines in the meridian plane are contours of the
stream function psi = rho * A_phi, evaluated in closed form via complete
elliptic integrals (computed with the arithmetic-geometric mean). Contour
levels are chosen so lines cross the midplane at evenly spaced heights, so
line spacing is flux-true: even spacing in the bore IS the field uniformity.

Configuration lineage: angular positions (40.09 deg, 73.43 deg) are the
fourth-order cancellation roots of Fanselau (1929); the sphere-constrained
solution with ampere-turn ratio 0.68211 cancels the 2nd, 4th and 6th order
terms (Garrett 1951; Fiorillo 2005, "double Helmholtz"). Gottardi et al.
(2003) first built it and coined "tetracoil" (integer NI ratio 73:107).

Primary reference: Gottardi et al., Bioelectromagnetics 24(2), 125-133
(2003). DOI: 10.1002/bem.10074

Licence: MIT (code); generated figures CC-BY-4.0.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Config:
    """Geometry (normalised to inner coil radius = 1) and styling."""

    # --- tetracoil geometry, exact sphere-constrained values -------------
    THETA_OUTER_DEG = 40.09          # Fanselau root, outer pair
    THETA_INNER_DEG = 73.43          # Fanselau root, inner pair
    NI_RATIO = 0.68211               # ampere-turns outer/inner (73:107)

    # --- figure ----------------------------------------------------------
    EXTENT = 1.75                    # half-width of plotted region
    GRID_N = 1100                    # stream-function grid resolution
    N_LINES = 16                     # field lines crossing the midplane
    MIDPLANE_Y = (0.09, 1.62)        # heights of first/last line at x = 0
    ARROW_FRACTIONS = (0.28, 0.78)   # arc-length positions of arrowheads
    UNIFORM_RADIUS = 0.56            # 1 % uniformity sphere (filament model)

    # --- Okabe-Ito colour-blind-safe palette ------------------------------
    C_LINE = "#222222"
    C_OUT = "#D55E00"                # current out of page (vermillion)
    C_IN = "#0072B2"                 # current into page (blue)
    C_REGION = "#009E73"             # uniform-region marker (bluish green)

    OUT_STEM = "tetracoil_field_lines"


def ellipk_e(m):
    """Complete elliptic integrals K(m), E(m) via AGM; m = k^2 in [0, 1)."""
    a, b, c = np.ones_like(m), np.sqrt(1.0 - m), np.sqrt(m)
    s, p = 0.5 * c**2, 1.0
    for _ in range(60):
        a, b, c = (a + b) / 2.0, np.sqrt(a * b), (a - b) / 2.0
        p *= 2.0
        s += 0.5 * p * c**2
        if np.max(c) < 1e-15:
            break
    K = np.pi / (2.0 * a)
    return K, K * (1.0 - s)


def coil_set(cfg):
    """Return [(radius, axial position, ampere-turns), ...] for the tetracoil."""
    t1, t2 = np.radians(cfg.THETA_OUTER_DEG), np.radians(cfg.THETA_INNER_DEG)
    s1, c1, s2, c2 = np.sin(t1), np.cos(t1), np.sin(t2), np.cos(t2)
    a_out, x_out = s1 / s2, c1 / s2      # 0.67187, 0.79822
    x_in = c2 / s2                        # 0.29758
    k = cfg.NI_RATIO
    return [(a_out, -x_out, k), (1.0, -x_in, 1.0), (1.0, x_in, 1.0), (a_out, x_out, k)]


def stream_psi(coils, X, Y):
    """Stream function psi = rho*A_phi; contours of psi are field lines."""
    rho = np.maximum(np.abs(Y), 1e-9)
    psi = np.zeros_like(X, dtype=float)
    for a, x0, I in coils:
        z = X - x0
        m = np.clip(4 * a * rho / ((a + rho)**2 + z**2), 1e-12, 1 - 1e-12)
        K, E = ellipk_e(m)
        psi += rho * I / (np.pi * np.sqrt(m)) * np.sqrt(a / rho) * ((1 - m / 2) * K - E)
    return psi


def field_at(coils, x, y):
    """(Bx, By) at a point in the meridian plane (axis = x)."""
    rho = max(abs(y), 1e-9)
    Bx = By = 0.0
    for a, x0, I in coils:
        z = x - x0
        q = (a + rho)**2 + z**2
        m = np.clip(4 * a * rho / q, 1e-12, 1 - 1e-12)
        K, E = ellipk_e(np.array([m]))
        K, E = K[0], E[0]
        den = (a - rho)**2 + z**2
        Bx += I / (2 * np.pi * np.sqrt(q)) * (K + (a**2 - rho**2 - z**2) / den * E)
        Br = I * z / (2 * np.pi * rho * np.sqrt(q)) * (-K + (a**2 + rho**2 + z**2) / den * E)
        By += np.sign(y) * Br
    return Bx, By


def add_arrows(ax, cfg, coils, contour_set):
    """Place arrowheads along each contour path, oriented by the local field."""
    line_idx = 0
    for collection_paths in contour_set.allsegs:
        for seg in collection_paths:
            line_idx += 1
            stagger = 0.07 * (line_idx % 3 - 1)
            if len(seg) < 8:
                continue
            d = np.hypot(np.diff(seg[:, 0]), np.diff(seg[:, 1]))
            arc = np.concatenate([[0.0], np.cumsum(d)])
            if arc[-1] < 0.6:
                continue
            closed = np.hypot(*(seg[0] - seg[-1])) < 1e-3
            fractions = (0.5,) if closed or arc[-1] <= 2.0 else cfg.ARROW_FRACTIONS
            for f in fractions:
                f = min(max(f + stagger, 0.05), 0.95)
                i = int(np.searchsorted(arc, f * arc[-1]))
                i = min(max(i, 1), len(seg) - 2)
                p = seg[i]
                if max(abs(p[0]), abs(p[1])) > 0.96 * cfg.EXTENT:
                    continue
                if min(np.hypot(p[0] - x0, abs(p[1]) - a) for a, x0, _ in coils) < 0.30:
                    continue
                bx, by = field_at(coils, p[0], p[1])
                nrm = np.hypot(bx, by)
                if nrm == 0:
                    continue
                ux, uy = bx / nrm, by / nrm
                ax.annotate("", xy=(p[0] + 0.01 * ux, p[1] + 0.01 * uy), xytext=(p[0], p[1]),
                            arrowprops=dict(arrowstyle="-|>", color=cfg.C_LINE,
                                            mutation_scale=11, lw=0))


def draw(cfg=Config()):
    coils = coil_set(cfg)

    n = cfg.GRID_N
    xs = np.linspace(-cfg.EXTENT, cfg.EXTENT, n)
    X, Y = np.meshgrid(xs, xs)
    PSI = stream_psi(coils, X, Y)

    # levels chosen so lines cross the midplane at evenly spaced heights
    y_mid = np.linspace(*cfg.MIDPLANE_Y, cfg.N_LINES)
    levels = np.sort(stream_psi(coils, np.zeros_like(y_mid), y_mid))

    fig, ax = plt.subplots(figsize=(7, 7))
    cs = ax.contour(X, Y, PSI, levels=levels, colors=cfg.C_LINE, linewidths=0.9)
    add_arrows(ax, cfg, coils, cs)

    # coil cross-sections: out of page (top) / into page (bottom)
    for a, x0, I in coils:
        ms = 9 + 4 * I
        ax.plot(x0, a, "o", ms=ms, mfc="white", mec=cfg.C_OUT, mew=1.6, zorder=5)
        ax.plot(x0, a, ".", ms=4, color=cfg.C_OUT, zorder=6)
        ax.plot(x0, -a, "o", ms=ms, mfc="white", mec=cfg.C_IN, mew=1.6, zorder=5)
        d = 0.028
        ax.plot([x0 - d, x0 + d], [-a - d, -a + d], color=cfg.C_IN, lw=1.4, zorder=6)
        ax.plot([x0 - d, x0 + d], [-a + d, -a - d], color=cfg.C_IN, lw=1.4, zorder=6)

    th = np.linspace(0, 2 * np.pi, 200)
    r = cfg.UNIFORM_RADIUS
    ax.plot(r * np.cos(th), r * np.sin(th), ls="--", lw=1.0, color=cfg.C_REGION, alpha=0.9)
    ax.text(0, -r - 0.12, "1% uniform region", ha="center", fontsize=8, color=cfg.C_REGION)

    ax.set_xlim(-cfg.EXTENT, cfg.EXTENT)
    ax.set_ylim(-cfg.EXTENT, cfg.EXTENT)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.tight_layout(pad=0.2)

    import os
    outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    os.makedirs(outdir, exist_ok=True)
    for ext in ("svg", "png"):
        path = os.path.join(outdir, f"{cfg.OUT_STEM}.{ext}")
        fig.savefig(path, dpi=200, facecolor="white")
        print(f"saved {path}")


if __name__ == "__main__":
    draw()
