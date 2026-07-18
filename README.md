# Tetracoil Magnetic Field Visualisation

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT%20%2F%20CC--BY--4.0-orange?style=flat-square)](LICENSE.md)
[![University](https://img.shields.io/badge/University-Warwick-green?style=flat-square)](https://warwick.ac.uk/)
[![Status](https://img.shields.io/badge/Status-Research-lightgrey?style=flat-square)](https://github.com/topics/research)

A self-contained Python script (numpy + matplotlib only) that draws the magnetic field of the tetracoil, a four-coil arrangement designed to produce a highly uniform field in its bore. The field lines are exact: they are contours of the stream function computed in closed form via elliptic integrals, spaced so their density is a true picture of the field, with direction arrowheads and a colour-blind-safe palette.

This came out of a third-year individual research project at Warwick (ES327, 2024/25, supervised by Dr Richard L. Watson) characterising a four-coil uniform-field system. The visualiser is the open, reproducible figure generator for that work.

![Tetracoil magnetic field](output/tetracoil_field_lines.svg)

*Magnetic field lines of the tetracoil, showing the uniform central region and the characteristic field topology.*

## Background

The tetracoil is the single-sphere, two-pair coil system whose angular positions (40.09°, 73.43°) are the fourth-order cancellation roots found by Fanselau (1929). The sphere-constrained solution, with an ampere-turn ratio of 0.68211, cancels the 2nd, 4th, and 6th order field terms (an 8th-order system) and appears in Garrett (1951) and in Fiorillo (2005, Ch. 4, as the "double Helmholtz coil"). Gottardi et al. (2003) first built it physically and coined the name "tetracoil".

Field lines in the meridian plane of an axisymmetric system are level sets of the stream function ψ = ρ·A_φ, which this implementation evaluates in closed form using complete elliptic integrals (AGM method). Contour levels are chosen so lines cross the midplane at evenly spaced heights, making the spacing flux-true: even spacing in the bore is itself a picture of the field uniformity. Output is publication-quality SVG and PNG.

## Quick start

```bash
git clone https://github.com/AdzCoder/tetracoil-field-visualisation.git
cd tetracoil-field-visualisation
pip install -r requirements.txt
python src/tetracoil_field.py
```

SVG and PNG are written to `output/`. Parameters at the top of `src/tetracoil_field.py` control field-line density, the plotted region, coil positioning, arrow styling, and output resolution.

## Requirements

- **Python** 3.8 or later
- **NumPy** and **Matplotlib**, nothing else

## Licensing

Dual-licensed to separate the code from the figures it produces:

- **Source code** (`src/tetracoil_field.py`): [MIT](LICENSES/MIT.txt)
- **Generated visualisations** (`output/`): [Creative Commons Attribution 4.0](LICENSES/CC-BY-4.0.txt)

## Citation

```bibtex
@software{bhatti2025tetracoil,
  author  = {Bhatti, Adil Wahab},
  title   = {Tetracoil Magnetic Field Visualisation},
  year    = {2025},
  url     = {https://github.com/AdzCoder/tetracoil-field-visualisation},
  version = {2.0.0}
}
```

## References

- Gottardi, G., Mesirca, P., Agostini, C., Remondini, D., & Bersani, F. (2003). A four coil exposure system (tetracoil) producing a highly uniform magnetic field. *Bioelectromagnetics*, 24(2), 125-133. [DOI: 10.1002/bem.10074](https://doi.org/10.1002/bem.10074)
- Fanselau, G. (1929). Die Erzeugung weitgehend homogener Magnetfelder durch Kreisströme. *Zeitschrift für Physik*, 54, 260-269. [DOI: 10.1007/BF01339844](https://doi.org/10.1007/BF01339844)
- Garrett, M.W. (1951). Axially symmetric systems for generating and measuring magnetic fields. *Journal of Applied Physics*, 22(9), 1091-1107. [DOI: 10.1063/1.1700115](https://doi.org/10.1063/1.1700115)
- Fiorillo, F. (2005). Chapter 4 — Magnetic Field Sources. In *Characterization and Measurement of Magnetic Materials*. Elsevier. [DOI: 10.1016/B978-012257251-7/50006-X](https://doi.org/10.1016/B978-012257251-7/50006-X)

## Author

**Adil Wahab Bhatti** ([@AdzCoder](https://github.com/AdzCoder)), University of Warwick. With thanks to Dr Richard L. Watson (ES327 supervisor) and to Gottardi et al. for the original tetracoil work.

---

*Developed as part of a third-year research project at the University of Warwick.*
