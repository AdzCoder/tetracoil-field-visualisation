# References and Background

## Primary Reference

Gottardi, G., Mesirca, P., Agostini, C., Remondini, D., & Bersani, F. (2003).
A four coil exposure system (tetracoil) producing a highly uniform magnetic field.
_Bioelectromagnetics_, 24(2), 125-133. DOI: 10.1002/bem.10074

## Configuration Lineage

The tetracoil geometry predates its name. The angular positions (40.09 deg,
73.43 deg) are the fourth-order cancellation roots derived by Fanselau (1929);
the single-sphere solution with ampere-turn ratio 0.68211 (approx. 73:107)
cancels the 2nd, 4th and 6th order field terms and appears in Garrett (1951),
and in Fiorillo (2005, Ch. 4) as the "double Helmholtz coil". Gottardi et al.
(2003) first built the system and coined "tetracoil".

- Fanselau, G. (1929). Die Erzeugung weitgehend homogener Magnetfelder durch
  Kreisstroeme. _Zeitschrift fuer Physik_, 54, 260-269. DOI: 10.1007/BF01339844
- Garrett, M.W. (1951). Axially symmetric systems for generating and measuring
  magnetic fields. _Journal of Applied Physics_, 22(9), 1091-1107.
  DOI: 10.1063/1.1700115
- Fiorillo, F. (2005). Chapter 4 - Magnetic Field Sources. In _Characterization
  and Measurement of Magnetic Materials_. Elsevier.
  DOI: 10.1016/B978-012257251-7/50006-X

## Technical Implementation

- Self-contained renderer: exact field lines as stream-function
  contours, elliptic integrals via the arithmetic-geometric mean; numpy and
  matplotlib only. MIT licence for code, CC-BY-4.0 for outputs.
- Okabe-Ito colour-blind-safe palette for publication figures.
