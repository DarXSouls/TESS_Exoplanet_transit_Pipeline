# Experimental validation notes

> **Reproducibility note:** The figures below are carried over from project-development notes supplied with this repository snapshot. The current snapshot does not include the complete transit-fitting, difference-image, or uncertainty-aware vetting implementation needed to reproduce these results end to end. Treat these as reported exploratory results, not as a benchmark independently verified from the code currently published here.

## 1. Dilution and planetary-radius fitting
On WASP-126 b (TIC 25155310), my initial fits were under-reporting planetary radius (~8.7 R⊕ vs the true 10.65 R⊕). Why? In crowded stellar fields, background flux dilutes the transit depth. Implementing aperture level CROWDSAP deblending and limb-darkened Mandel & Agol transit models brought the fitted radius to 10.70 ± 0.54 R⊕ (0.953 R_Jup) — within <0.5% of discovery literature! 🎯

## 2. Frequency-uniform period search
Box Least Squares (BLS) kept getting harmonic-locked onto 2x orbital periods (reporting 6.57 d instead of 3.28 d). Upgrading to a 25,000-point uniform-frequency grid (Δν = const) with automated depth doubling subharmonic tests completely eliminated period aliasing.

## 3. Pixel-level difference-image analysis
To weed out background blended eclipsing binaries (NEBs), I built a sub-pixel DIA engine that computes the flux-weighted centroid offset between in-transit and out-of-transit frames. WASP-126 b passed cleanly at Δr = 0.0043 pixels (< 0.01 px threshold).

## 4. Uncertainty-aware candidate vetting
The biggest breakthrough was handling grazing transits (impact parameter b > 0.9). A point-estimate threshold isn't enough when a candidate's 1-sigma posterior spans both planetary and stellar regimes. 
The pipeline now evaluates the full 16th–84th percentile posterior credible interval:
- Rp,84 < 25 R⊕ ➔ Confident CANDIDATE (100% prob)
- 1-sigma spans 25 R⊕ boundary or b > 0.95 ➔ AMBIGUOUS (50% prob, flags BLS_MCMC_DEPTH_MISMATCH)
- Rp,16 > 25 R⊕ ➔ Confident FALSE_POSITIVE (0% prob, flags FAILED_PLANETARY_RADIUS_CEILING)

### Reported multi-target validation results
- WASP-126 b (Confirmed Planet): Period = 3.2888 d, Rp = 10.70 R⊕ (<0.5% error) ➔ CANDIDATE ✅
- TOI-628 b (Confirmed Planet): Period = 3.4095 d, Rp = 11.42 R⊕ (exact match) ➔ CANDIDATE ✅
- TOI-1365.01 (Grazing False Positive, b = 0.92): Ratio = 1.50x ➔ AMBIGUOUS (flagged near-grazing) ⚠️
- TOI-1168.01 (Grazing False Positive, b = 0.96): Rp = 23.86 R⊕ ➔ AMBIGUOUS ⚠️
- TOI-959.01 (Certified Eclipsing Binary): Fitted Rp = 59.58 R⊕ ➔ FALSE_POSITIVE (0.00%) ❌

Finding candidate dips is the easy part. Building an automated system that understands Bayesian posteriors, noise floors, and astrophysical degeneracies well enough to NOT produce false confidence is where the real science lives.