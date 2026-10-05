# Where Model Error Should Live: Project Design Document — v3

**Context:** Applied AI master's, 3-month project, **three people**
**Supersedes:** v2 (six RQs, seven methods, undefined forcing, 11-week experiment window)
**Status:** ready for supervisor review

---

## Table of contents

1. [What changed from v2, and why](#1-what-changed-from-v2-and-why)
2. [The reframe: where model error lives](#2-the-reframe-where-model-error-lives)
3. [Why this project — reasoning and the assertions it rests on](#3-why-this-project--reasoning-and-the-assertions-it-rests-on)
4. [Final plan](#4-final-plan)
5. [Data sources](#5-data-sources)
6. [Software, tooling and resources](#6-software-tooling-and-resources)
7. [Appendix A: governing equations](#appendix-a-governing-equations)
8. [Appendix B: discarded options and why](#appendix-b-discarded-options-and-why)
9. [Appendix C: references](#appendix-c-references)

---

## 1. What changed from v2, and why

Seven changes. The first three are structural; the rest follow from them.

| # | Change | Reason |
|---|---|---|
| 1 | **Core question reframed as a discrepancy-treatment comparison (L0–L3), not a PINN-vs-classical shootout** | v2's RQ2 ("does the PINN silently absorb model error?") was answered in general form by Kennedy & O'Hagan (2001) and Brynjarsdóttir & O'Hagan (2014), and in PINN-specific form by Zou, Meng & Karniadakis (2024). None of them compare *implicit* network flexibility against *explicit* discrepancy modelling, and none use a structured discrepancy grounded in a real instrument. That gap is now the project. |
| 2 | **Measurement modality decided: resonance frequency + mode shape. Not deferred to week 1.** | v2's inversion model carried an undefined load `q(x)`. Worse, the two static alternatives cannot recover E at all: a released cantilever's stress-gradient arc is `w = κ₀x²/2` with E cancelled, and Euler buckling of a bridge gives residual strain with E cancelled. This is precisely why ASTM E 2245/2246 report strain and strain gradient while SEMI MS4 reports modulus from resonance. The modality was never actually open. |
| 3 | **Experiments stop at week 8; weeks 9–11 are executive summary and presentation** | v2 ran experiments to week 11 and left one week for three people to write. The programme calendar is 11 weeks with fixed weekly deliverables (§4.12); freeing week 2 from convenio paperwork restores the engineering time the shorter calendar costs. |
| 4 | **RQ3 (field σ₀(x) + Tikhonov) deleted; demoted to future work** | A second study, least connected to the core question, and the most crowded — Teloli et al. already recover spatially varying material properties in Euler–Bernoulli beams with PINNs. Deleting it pays for change 3. |
| 5 | **M1 gains a translational anchor spring k_u; M2 replaced by Timoshenko shear and rotary inertia** | Kobrinsky's support model responds to both forces *and* moments, and axial anchor compliance is the mechanism that generates length-dependent apparent properties. Mid-plane stretching is a large-amplitude *static* effect with no meaning in a small-amplitude modal measurement; shear deformation and rotary inertia are the real missing terms for short beams and higher modes. |
| 6 | **Two reference posteriors instead of one; PINN written in mixed (w, M) form** | MCMC over the *misspecified* model answers the wrong question on its own. And four nested autodiff passes for `w''''` is slow and ill-conditioned — a known failure mode v2 did not budget for. |
| 7 | **Real-data arm split in two; squeeze-film named as the G0 pivot; the regimes where PINNs genuinely win stated explicitly** | The frequency modality recovers E but has no dense spatial data; the strain structures have dense traces but identify σ₀ and κ₀ instead. Running both removes the dependency on a single data case (§4.10). §3.1.1 and §3.1.2 pre-empt the two questions a reviewer will ask first: *why not high dimensions or design, where PINNs are supposed to win?* and *why this device?* |

---

## 2. The reframe: where model error lives

### 2.1 The one-paragraph version

Every method that extracts a physical parameter from data assumes a forward model. That model is always somewhat wrong. The methods differ in **what they do about it** — and that, not the choice of optimizer or the presence of a neural network, is what determines whether the extracted parameter is trustworthy. This project lines up four treatments of model error on a single measurement problem with a documented, quantified error source, and asks which one you should actually use.

### 2.2 The discrepancy ladder

| Level | Treatment of model error | Instantiations here |
|---|---|---|
| **L0** | **Ignored.** The assumed model is treated as exact. | SEMI MS4 closed form; nested least squares over the eigensolver; PINN at fixed high λ_PDE |
| **L1** | **Implicit and undeclared.** No discrepancy term exists, but the fitted solution field is free to depart from the PDE. Model error is absorbed silently, wherever the optimizer puts it. | PINN with relaxed λ_PDE; PINN with adaptive/learned λ_PDE |
| **L2** | **Explicit but unstructured.** A named, flexible term absorbs the mismatch, with no prior knowledge of its form. | PINN + discrepancy network δ(ξ) added to the residual (Zou et al. 2024); classical LSQ + smooth discrepancy basis |
| **L3** | **Explicit and structured.** The form of the error is known; its magnitude becomes an extra unknown. | k_θ and k_u fitted alongside E and σ₀, both classically and in the PINN |

L0 is the incumbent. L2 is published state of the art. **L1 is the one nobody has characterized**, and it is what you get by default when you train a PINN on real data and relax the physics weight because training is unstable — which practitioners do constantly. L3 is the arm a MEMS metrologist would actually want.

### 2.3 Why this is a real question and not a relabelling

- **Against KOH:** the statistics literature treats discrepancy as something you either model or don't. L1 is a third thing — flexibility with no declared discrepancy term, no prior, and no uncertainty attached to it. Brynjarsdóttir & O'Hagan showed that explicit discrepancy modelling still biases parameters unless you know the discrepancy form. Nobody has asked what *undeclared* flexibility does by comparison.
- **Against Zou et al.:** they propose L2 and show it works. They do not quantify the L0→L1 bias their method is designed to remove, do not compare against L3, and do not test on a standardized measurement with a published uncertainty budget.
- **Against the PINN-vs-FEM literature:** that debate is about forward accuracy and wall-clock time. This is about estimator bias under a wrong model, where the forward solve is cheap and speed is not the axis of interest.

### 2.4 What each outcome means

| Result | Interpretation | Useful to whom |
|---|---|---|
| L1 ≈ L0 | The network's flexibility does nothing; relaxing λ_PDE is cosmetic | PINN practitioners — stop doing it |
| L1 ≈ L2 | Undeclared flexibility is as good as an explicit discrepancy term, at lower cost | Strongest positive result available |
| L1 worse than L0 | Flexibility actively harms the estimate; the physics term was load-bearing | Practitioner warning, arguably the most valuable outcome |
| L3 ≫ all | Knowing the error's form beats every generic treatment | MEMS metrology — use the corrected extraction |

There is no configuration of results that produces a non-thesis. That is the point of the design.

---

## 3. Why this project — reasoning and the assertions it rests on

### 3.1 The argument in one chain

1. Extracting Young's modulus and residual stress from micromachined beam test structures is a real, standardized, industrially used measurement.
2. The extraction is an inverse problem in which the forward model is known to be slightly wrong, most reliably because the anchors are not perfectly rigid — a named line item in NIST's own uncertainty budget.
3. Methods differ in how they treat that wrongness, and those treatments form an ordered ladder (L0–L3) that has never been benchmarked end to end.
4. The benchmark has a clean experimental design (generate from a richer model, invert with treatments of varying honesty), a strong incumbent (an international standard test method), a Bayesian reference that separates estimator bias from model-form bias, and a real-data validation path.
5. It produces a useful answer whichever way it comes out.

Note what is **not** claimed: that PINNs have a structural advantage here. For a 1D beam with two scalar unknowns and a millisecond forward solve, the classical nested loop is cheaper and the "single optimization" argument is illusory. This problem is chosen because it is a **clean, well-instrumented testbed for the discrepancy question**, not because it flatters the method under test. Say this in the introduction before a reviewer says it for you.

### 3.1.1 Where PINNs genuinely do win, and why we are not there

A reviewer will ask why we chose the regime least favourable to the method. Answer it in the introduction, in three sentences, rather than defending it in the viva.

| Regime where PINNs win | Why it is not this project |
|---|---|
| **High dimension (3D+, or hundreds of dimensions in filtering and control)** | Grossmann et al. name this explicitly — PINNs avoid the exponential cost of mesh generation. But **in that regime there is no reference solution to check against**, which is the very reason one reaches for a PINN. A thesis there has no ground truth, no error metric, and no defensible accuracy claim. MEMS also does not supply such problems: it supplies 2D/3D solid mechanics with electrostatics, where FEM is strongest. |
| **Complex or awkward geometry** | The real competitors are cut-cell FEM, meshfree methods and isogeometric analysis, not plain FEM. The advantage is in *setup effort*, not accuracy — arXiv:2509.20191 found precisely that: less human effort and specialist knowledge required, and still outperformed. Building a genuinely nasty MEMS geometry needs CAD, meshing and a FEM reference, and COMSOL and ANSYS are both ruled out (§6.3). |
| **Design surrogacy — train once, evaluate a million times** | The competitor is a Gaussian process on a few hundred FEM runs, which typically wins on accuracy, trains in seconds, and supplies uncertainty bounds for free. Generating those runs requires the FEM solver we do not have. And the framing loses both of our strongest assets: no standardized incumbent and no free real data, which returns us to the inverse-crime problem. |

**One caveat worth stating rather than hiding:** dimension can live in the *parameter* space rather than the physical space. A parametric PINN over many design variables is a high-dimensional problem in a meaningful sense, and our shared-parameter network across multiple structures (§4.6, Method 3) is a small instance of it. We do not claim to test that regime; we note it as the natural extension of this work.

### 3.1.2 Why this device and not another

The beam test structure was not chosen for being the most interesting MEMS device. It was chosen for being the only candidate that scores on **all four** requirements at once.

| Device | Cheap forward model | Documented model error | Free real data | Standard incumbent |
|---|---|---|---|---|
| **Beam test structure** | ✔ | ✔ | ✔ | ✔ |
| Squeeze-film damping, rarefied regime | ✔ | ✔✔ | partial | ✘ |
| Pull-in / M-TEST | ✘ (limit point) | ✔ | ✔ | partial |
| Thermal microhotplate | ✔ | ✔ | ✘ | ✘ |
| Accelerometer / gyroscope | ✘ (3D modal FEM) | ✔ | ✘ | ✘ |
| PMUT (piezoelectric) | ✘ | ✔ | ✘ | ✘ |

**Squeeze-film damping is the named fallback if G0 fails.** In the rarefied regime the Reynolds equation is known to be wrong, and there are *several competing named corrections* — first-order slip, second-order slip, Fukui–Kaneko. That is unusually good for this project's structure: L3 gains three candidate forms instead of one, which upgrades it from a correction to a **model-selection** question, and L2 keeps its meaning unchanged.

What is lost: no SEMI or ASTM standard, so the incumbent can be called a strawman; and no NIST round-robin, so the real-data arm weakens to scattered published measurements. Those two assets are what make the current plan defensible, which is why squeeze-film stays in reserve rather than in the plan. **If G0 fails on data usability, pivot here rather than retreating to a synthetic-only study** — the ladder, the two posteriors, the harness and the analysis code all transfer unchanged.

### 3.2 Assertions this project rests on

**A1. For correct-model forward problems, classical numerical methods beat PINNs on accuracy and time.**
*Source:* Grossmann, Komorowska, Latz & Schönlieb (2024), *IMA J. Appl. Math.* 89(1), 143–174, DOI 10.1093/imamat/hxae011. **Verified.**
*Note:* Their study covers forward problems only (Poisson 1D/2D/3D, Allen–Cahn, semilinear Schrödinger). They explicitly flag inverse problems and data integration as where PINNs remain complementary. This supports the framing rather than undermining it.
*Role:* Makes H0 a pipeline validation check, not a hypothesis.

**A2. PINN failure under increasing difficulty is an optimization-landscape phenomenon, not an expressivity limit.**
*Source:* Krishnapriyan, Gholami, Zhe, Kirby & Mahoney (2021), *NeurIPS* 34.
*Confidence:* High.
*Role:* Predicts that failures look like training stalls and seed-dependent variance. Success rate across seeds must be reported and failure defined explicitly.

**A3. ML-for-PDEs comparisons have historically used weak baselines, and reviewers now probe this.**
*Source:* McGreivy & Hakim (2024), *Nature Machine Intelligence*.
*Confidence:* High.
*Role:* Baseline tuning effort documented per method, one paragraph each. L0 must be the real SEMI MS4 procedure, not a cartoon of it.

**A4. Anchor compliance is a documented, quantified error source in beam-based property extraction.**
*Sources:* NIST SP 260-177 carries σ_support, an explicit uncertainty term for non-ideal support or attachment conditions, alongside σ_cantilever. Kobrinsky, Deutsch & Senturia (2000), *JMEMS* 9(3), 361–369 — **verified**; their elastic model takes support response to *both forces and moments* from FEM, and explains a previously observed gradual increase in beam deflection with increasing length at constant residual stress.
*Confidence:* High.
*Role:* Grounds M1, motivates the k_u spring, and supplies the L3 arm's structure. Their length-trend result is the template for A8.

**A5. PINNs are outperformed by classical methods on inverse problems even without misspecification.**
*Source:* Jekic et al. (2025), arXiv:2509.20191, NTNU/SINTEF. **Verified, and v2's description was wrong.** The paper compares PINNs against FEM plus a numerical optimizer on increasingly difficult fluid mechanics problems (Burgers, Navier–Stokes), with and without noise, and finds PINNs outperformed by the traditional approach despite requiring less human effort and specialized knowledge.
*Confidence:* High for the headline; the bias and adaptive-weighting claims in v2 need checking against the body text.
*Role:* No longer the main novelty threat. It is correct-model, fluid mechanics, noise-only, no real data, no reference posterior. It *does* pre-empt any naive "PINNs win" claim, which the L0–L3 framing avoids making.

**A6. The closest genuine neighbour is Zou, Meng & Karniadakis (2024).**
*Source:* *J. Comput. Phys.* 505, 112918, DOI 10.1016/j.jcp.2024.112918. **Verified.** They encode possibly-misspecified physical models in PINNs, then use additional DNNs to model the discrepancy between imperfect model and observational data, with B-PINNs or ensemble PINNs for uncertainty, demonstrated on reaction–diffusion and non-Newtonian flows.
*Confidence:* High.
*Role:* **This is L2.** It must be cited in the introduction, implemented as a comparator, and differentiated: they propose a correction, we characterize the ladder that correction sits on.
*If we fail to differentiate:* the novelty claim collapses. This is now the single largest novelty risk, replacing A5.

**A7. The statistical foundation of the bias phenomenon is the KOH identifiability problem.**
*Sources:* Kennedy & O'Hagan (2001); Brynjarsdóttir & O'Hagan (2014). Without a discrepancy term, calibration forces the model to fit the data even when the structure is wrong, producing biased parameter estimates; with one, θ and δ are not jointly identifiable, and the bias is only reliably reduced by knowing the discrepancy form a priori.
*Confidence:* High.
*Role:* Gives the project a theoretical spine and a **prediction to test**, not just a phenomenon to observe: L3 should beat L2 because L3 knows the form. If that fails, something interesting happened.

**A8. Anchor compliance predicts a specific functional form of apparent-E drift with beam length.**
*Reasoning:* Young's modulus is a material property and cannot depend on how long the cantilever was drawn. A compliant anchor is equivalent to a small length extension ΔL, so the apparent modulus from a resonance measurement scales as `E_app/E_true ≈ (L/(L+ΔL))⁴` — a steep, monotone, one-parameter curve. Kobrinsky et al. report exactly this class of length trend from support compliance.
*Confidence:* High on the logic. **Unverified on whether NIST's data shows it.**
*Role:* This is the real-data chapter. Not "look, there's drift" — *fit the predicted one-parameter curve to NIST's E-versus-length data and report ΔL with a confidence interval.* That is falsifiable, it reproduces a published mechanism, and it is the most publishable object in the project.
*Caveat to state in writing:* apparent drift can also come from extraction ill-conditioning and from layout-correlated process variation. The curve-fit test is what distinguishes the hypotheses.
*Action:* Inspect Figs. YM-series and RS10/SG10 in week 2 (G0). Task #1.

**A9. Usable real measurement data is publicly available at no cost.**
*Source:* NIST SP 260-177 (free, DOI 10.6028/NIST.SP.260-177) and NIST SRD 166 (MEMS Calculator).
*Confidence:* High for existence. **Medium for usability** — the guide reports derived quantities per structure and round-robin repeatability/reproducibility tables, not necessarily dense mode shapes.
*Consequence:* The real-data arm inverts from *a set of structures of varying length* rather than from a dense profile of one structure. Under the frequency modality this is natural, not a compromise: the length sweep *is* the A8 test.
*Gate:* G0, week 1.

**A10. The MEMS content is a testbed, not the subject.**
*Confidence:* Scoping decision, not a fact.
*Role:* The thesis needs the beam equation, the measurement context, and one motivation section.
*Action:* Confirm with the supervisor in week 1.

### 3.3 What makes it useful (as distinct from valuable)

- The measurement is standardized by SEMI and ASTM, validated by NIST round-robin, and used for wafer-level process monitoring.
- The error source under study is a named line item in the standard's own uncertainty budget.
- **The L3 arm is directly actionable:** if fitting k_θ and k_u alongside E measurably reduces the length-dependence of extracted modulus, that is a correction a metrologist can adopt.
- A method that can *signal* "your model doesn't fit this data" is useful even if it loses on accuracy — hence the residual-diagnostic metric.
- RQ4 (placement) is a zero-cost recommendation if it lands.

**Be honest about which part is most useful.** The highest-value practical output may be a MEMS metrology result ("apparent modulus drifts with length by X%, consistent with ΔL = Y µm of anchor compliance") that is independent of whether any PINN wins anything. Promote it if the supervisor weighs usefulness.

### 3.4 Three questions for the supervisor, in writing, in week 1

1. **Is a characterization or diagnosis result acceptable, or must the PINN beat something?** Ask directly: *"Would a thesis concluding that undeclared network flexibility is worse than doing nothing, with evidence, be acceptable?"*
2. **Is MEMS understood as a testbed rather than the subject?** (A10.)
3. **What is the expected page count, the writing window, and is this one joint document or three?** This determines whether the week-9 hard stop is early enough.

---

## 4. Final plan

### 4.1 Title (working)

*Declared versus undeclared model error: benchmarking discrepancy treatments for material-property extraction from MEMS beam test structures*

### 4.2 Research questions

**RQ1 (core).** Across the discrepancy ladder L0–L3, how does parameter error grow as misspecification severity increases? Produce a degradation curve per level.

**RQ2 (core).** Does L1's implicit flexibility behave like L0 (no effect), like L2 (equivalent to an explicit discrepancy term), or worse than both? Decomposed against two MCMC reference posteriors so that *estimator* bias and *model-form* bias are separated rather than confounded.

**RQ3.** Is λ_PDE the control knob that moves a PINN from L0 to L1, and does adaptive weighting land anywhere useful on that axis? *(This defines L1 operationally; it is not a side study.)*

**RQ4.** Does the *placement* of measurement points along the structure affect parameter recovery more or less than the choice of discrepancy treatment?

**RQ5 (validation).** Does the ladder's ordering hold on published real measurements, where the misspecification is real and unknown? Tested on **two independent arms** (§4.10): cantilever frequencies for E, and dense shape traces for σ0 and κ0. Does NIST's apparent-E-versus-length data fit the anchor-compliance curve predicted by A8, and do both arms imply the same ΔL?

### 4.3 Hypotheses

- **H0 (validation check).** With a correct model, classical least squares beats the PINN on accuracy and wall-clock time. Confirming this validates the pipeline. *(A1.)*
- **H1.** L0 error grows systematically and monotonically with severity (biased, low variance). This is the reference curve.
- **H2.** L1 shows lower bias than L0 but substantially higher variance across seeds, and the crossover severity is measurable.
- **H3.** L2 reduces bias relative to L0 but does not reach L3, because it lacks the discrepancy form. *(Directly predicted by A7.)*
- **H4.** L3 recovers E to within the round-robin reproducibility floor across the full severity range.
- **H5.** Placement changes parameter error by a margin comparable to the L0-to-L1 gap.

H2 failing — L1 being *more* biased than L0 — is a publishable practitioner warning and given A5 is at least as likely. **Write the abstract both ways in week 5 and see which one you'd rather defend.**

### 4.4 The physics

**Modality: resonance frequency and mode shape.** Decided. Justification in §1, change 2.

Inversion model — Euler–Bernoulli free vibration with axial load:

```
E·I·w''''(ξ) − N·w''(ξ) − ω²·ρA·w(ξ) = 0
N = σ₀·b·h,    I = b·h³/12,    A = b·h
```

**ω is measured data, not an unknown.** This is the key simplification. Because the mode shape is sampled at N points *and* the frequency is measured, the PINN never has to solve an eigenvalue problem — ω²ρA·w acts as a known forcing term that depends on w, the data loss pins the amplitude, and the trivial zero solution is excluded automatically. The classical baseline *does* solve the forward eigenproblem inside its optimization loop, which is the honest classical approach and keeps the comparison fair.

Boundary conditions:
- Cantilever: `w(0) = w'(0) = 0`, `M(L) = 0`, `M'(L) = 0`
- Clamped–clamped: `w(0) = w'(0) = w(L) = w'(L) = 0`

**Identifiability.** A released cantilever relaxes its axial stress, so N ≈ 0 and its frequency measures E nearly independently of σ₀. A clamped–clamped beam sustains N and its frequency is sensitive to both. Using both structures breaks the E/σ₀ degeneracy structurally. This is how it is done in practice. Additionally, **higher modes shift differently from the fundamental under anchor compliance**, so measuring ω₁, ω₂, ω₃ on the same structure gives an independent handle on k_θ — this is what makes the L3 arm identifiable at all.

**Non-dimensionalization is mandatory before any training.** Set `ξ = x/L`, `W = w/h`, group constants into dimensionless stiffness and tension parameters. MEMS units otherwise produce loss terms spanning 10+ orders of magnitude and training will not converge.

**Mixed formulation, from day one.** Do not compute `w''''` by four nested autodiff passes. Write the network with two outputs and the system as two second-order residuals:

```
r₁:  M − E·I·w''  =  0
r₂:  M'' − N·w'' − ω²ρA·w  =  0
```

Cheaper gradients, better conditioning, and — critically — the anchor-spring conditions become *essential* constraints on the second output M rather than awkward natural conditions on `w''`. This also makes the hard-versus-soft BC ablation symmetric and therefore meaningful.

**Reference solver: a generalized eigensolver, not `solve_bvp`.** Finite-difference or Rayleigh–Ritz discretization, `scipy.linalg.eigh`. `solve_bvp` is off the critical path entirely. No bifurcations, no limit points, no undefined loads anywhere in this design.

### 4.5 Misspecification ladder (data generation)

Data generated from a richer model; all treatments invert with the simple one above.

| Level | Added term in the generating model | Physical meaning | Status |
|---|---|---|---|
| **M0** | none | Correct model | Control |
| **M1** | rotational spring k_θ **and translational spring k_u** at each support | Anchor compliance — the documented failure mode | **Primary, dense sweep** |
| **M2** | Timoshenko: shear deformation + rotary inertia | Real for short/thick beams and higher modes | One severity |
| **M3** | linear thickness taper `h(ξ) = h₀(1 + α·ξ)` | Etch non-uniformity across the die | One severity |

**Severity is a continuous axis for M1 only.** Sweep the nondimensional compliance and report the **relative L2 difference between generating and inversion mode shapes plus the relative frequency shift** as the misspecification magnitude. Calibrate in week 2 so at least one point sits at the ≈5% systematic level reported in the M-TEST literature. M2 and M3 are single-point generalization checks: does the ladder's ordering survive a change of mechanism?

**k_θ and k_u should be derived, not assumed.** Off the critical path, one 2D plane-stress FEniCSx model of a beam-plus-anchor gives realistic values for a specific geometry. Roughly one person-week. Prefer citing Kobrinsky's published values if the schedule is tight.

### 4.6 Methods, organised by ladder level

| Level | # | Method | Role |
|---|---|---|---|
| **L0** | 1 | **SEMI MS4 closed form** via NIST MEMS Calculator (SRD 166) | **The true incumbent.** What industry runs today. |
| **L0** | 2 | **Classical nested inverse** — `least_squares` around the eigensolver | The strong classical baseline |
| **L0** | 3 | **PINN, fixed high λ_PDE** | PINN with the physics treated as exact |
| **L1** | 4 | **PINN, relaxed λ_PDE** (swept) | Implicit flexibility, manually dialled |
| **L1** | 5 | **PINN, adaptive/learned λ_PDE** | Implicit flexibility, automatic |
| **L2** | 6 | **PINN + discrepancy network δ(ξ)** (Zou et al. 2024) | Explicit, unstructured |
| **L2** | 7 | **Classical LSQ + smooth discrepancy basis** | The classical L2, so the level isn't PINN-only |
| **L3** | 8 | **Classical LSQ with k_θ, k_u as extra unknowns** | Explicit, structured |
| **L3** | 9 | **PINN with k_θ, k_u as trainable scalars** | Explicit, structured, in-network |
| **ref** | 10 | **Plain MLP**, no physics term | Isolates the physics term's contribution |
| **ref** | 11 | **MCMC ×2** (emcee or PyMC) over the Rayleigh–Ritz ROM | **Two reference posteriors.** See §4.7. |

**Internal PINN ablation:** soft-penalty versus hard-enforced BCs. In mixed form both essential and natural conditions hard-enforce cleanly, so the ablation is symmetric.

**Baseline tuning must be documented explicitly** — one paragraph per method: configurations tried, tolerances, ROM mode count, discrepancy basis size, λ selection, MCMC chain length and R̂. Cheap, and does disproportionate work in a defence (A3).

### 4.7 The two reference posteriors

This is what makes RQ2 answerable rather than arguable.

| Posterior | Forward model | What distance from it measures |
|---|---|---|
| **P_simple** | The L0 inversion model | **Estimator bias.** The correct Bayesian answer to the misspecified problem. A method far from P_simple's mean has an optimization or regularization pathology of its own. |
| **P_rich** | The L3 model, springs included | **Total error against the right problem.** The correct answer given knowledge of the discrepancy form. |

The **gap between the two posterior means is the irreducible cost of ignoring the discrepancy** — a single number per severity point, and the cleanest headline figure in the project.

Each point method is then placed on both axes. A method can be near P_simple and far from truth (faithfully solving the wrong problem) or far from both (broken). v2 conflated these.

**Do not use "does the point estimate fall inside the credible region" as a headline metric.** Under misspecification P_simple over-concentrates and every method fails that test at high severity, so it carries no signal. Report it once as an illustration of exactly that pathology, then move on.

Affordability: two scalar parameters, a Rayleigh–Ritz forward model at millisecond cost, standard samplers. Roughly 200 MCMC runs total. Trivial.

### 4.8 Experimental matrix

| Axis | Values | Notes |
|---|---|---|
| Misspecification mechanism | M0 (1) + M1 (6 severities) + M2 (1) + M3 (1) | **9 cells**, not 24 — severity is undefined at M0 and single-point for M2/M3 |
| Parameter set | E, σ₀ (scalar) | Field case deleted; see Tier 4 |
| Measurement count N | 5, 15, 40 | Per structure |
| Structures k | 1 (cantilever only), 3 (cantilever + bridge + second cantilever) | Tests the multi-structure identifiability claim |
| Modes measured | 1, 3 | Higher modes are the L3 identifiability handle |
| Seeds | 10 | Non-negotiable |
| Noise | fixed at 2% relative Gaussian | Held constant, not swept |

Core sweep: 9 cells × 3 N × 2 k × 2 modes × 10 seeds = **1080 runs per method**. Nine methods, but the three classical ones are near-instant, so the binding cost is ~5 PINN configurations ≈ 5400 PINN runs.

**Time a single PINN run at G3 and multiply before committing.** If a run exceeds one minute, cut in this pre-agreed order: (1) drop the modes axis to {3} only, (2) M1 severities from six to four, (3) N from three values to two. Do not improvise the cut at week 6.

RQ4 placement sub-study, separate and bounded: 3 placements × 2 severities × 4 methods × 10 seeds = 240 runs.

### 4.9 Metrics

**Accuracy**
- Relative error in E and σ₀
- Forward frequency prediction error on held-out structure lengths

**Bias vs variance (RQ2) — report separately, never collapsed into RMSE**
- Mean signed error across seeds, per ladder level, per severity
- Distance from P_simple mean (estimator bias) and from P_rich mean (total error)
- Posterior-mean gap as the irreducible-cost reference line

**Cost**
- Wall-clock to solution; forward eigensolves (classical) vs gradient steps (PINN)
- Break-even: after how many extraction tasks does the parametric PINN amortize?

**Robustness**
- Success rate across seeds, failure defined explicitly (>50% parameter error or non-convergence). Note that 10 seeds resolves success rate to ±10pp — report it, don't over-claim from it.
- Sensitivity to initial guess for all point methods

**Diagnostics**
- Classical: is the fit residual structured or noise-like? (Standard misspecification detector.)
- L1 PINN: does the PDE residual field carry the same signal, or has the flexibility erased the evidence? **If flexibility hides the symptom, that is the sharpest result in the project.**
- L2: does the learned δ(ξ) resemble the true discrepancy, or absorb unrelated variation?

### 4.10 Real-data arm (RQ5) — two arms, not one

Switching to the frequency modality (§1, change 2) moves the project *toward* NIST's data, not away from it: SEMI MS4 extracts Young's modulus from cantilever resonance, so NIST's published modulus values came from this modality. But the dense spatial traces in SP 260-177 belong to the *strain* structures, not the modulus ones. Rather than choosing, run both. Same physics, same code, same ladder, two independent validations of the same conclusion.

| | **Arm 1 — frequency** | **Arm 2 — shape** |
|---|---|---|
| Structures | Cantilevers of varying length (Tables YM1, YM7, YM8) | Fixed-fixed beams and curled cantilevers (Tables RS1, RS9, SG1, SG8; Figs. RS2c, RS3c, SG2c, SG3c) |
| Unknown | E | σ₀ (residual strain) and κ₀ (strain gradient) |
| Data density | One scalar per structure, across a length sweep | **Dense spatial traces along each beam** |
| Standard | SEMI MS4 | ASTM E 2245 / E 2246 |
| Tests | A8 anchor-compliance drift; L0–L3 ordering | L0–L3 ordering with full spatial residual diagnostics |

**Why the modulus cancellation does not hurt Arm 2.** E dropping out of the static arc and the buckling condition is only a problem if you are trying to recover E from them. Arm 2 recovers σ₀ and κ₀, which are exactly what those structures identify — and there the dense traces give the residual-diagnostic metrics (§4.9) real spatial data to work with, which Arm 1 cannot supply.

**Procedure**

1. Extract published measurements from NIST SP 260-177 (§5).
2. Reproduce one NIST data analysis sheet by hand via the MEMS Calculator. This *is* Method 1 and takes an afternoon.
3. Run the ladder on both structure sets.
4. **Test A8 quantitatively (Arm 1).** Fit `E_app/E_true = (L/(L+ΔL))⁴` to the apparent-modulus-versus-length data and report ΔL with a confidence interval. Compare against the σ_support term in NIST's own budget and against Kobrinsky's values. Report the alternative explanations (extraction conditioning, layout-correlated process variation) and what would distinguish them.
5. **Cross-check A8 (Arm 2).** Anchor compliance predicts drift in apparent residual strain and strain gradient with length too — Figs. RS10 and SG10. If the ΔL implied by Arm 2 agrees with Arm 1's, that is independent confirmation from a different measurement on the same chip. If they disagree, that is a finding worth a section.
6. Compare against the round-robin spread — repeatability from twelve cantilevers on one chip, reproducibility across eight participants, five laboratories, seven instruments and four chips. That spread is a real uncertainty floor no synthetic study produces, and it is the bar L3 must clear in H4.

**Arm 1 under the likely data case.** If SP 260-177 publishes only derived values and no mode shapes (A9, Medium confidence), Arm 1 still runs in a slightly unusual but defensible setup: the network predicts the mode shape for each beam length, the physics term constrains that shape, and the only data anchoring it is the single measured frequency per structure. Weakly supervised parameter identification across a structure family. State it as such — it is closer to how the standard actually works than a dense-profile inversion would be. Arm 2 is unaffected either way, which is the main reason it exists.

### 4.11 Team split

Three tracks by **layer**, plus one RQ each owned **end to end**, so every person has a defensible individual chapter.

| | Owns end-to-end | Weeks 2–5 | Weeks 6–7 | Weeks 8–11 |
|---|---|---|---|---|
| **A — Physics & reference** | RQ5 (real data) | Eigensolver; non-dimensionalization; analytical checks; M0–M3 generators; severity calibration; both MCMC posteriors | L2 classical discrepancy basis; M2/M3 generators finalized | Real-data arms 1 and 2; A8 curve fit |
| **B — PINN** | RQ1, RQ2 | Mixed-form PINN; forward validation; hard/soft BC ablation; L0 PINN | L1 sweep; λ_PDE study (RQ3); L2 discrepancy network | L3 in-network springs; residual diagnostics |
| **C — Classical & harness** | RQ3, RQ4 | Nested inverse; MEMS Calculator reproduction; config/seed/W&B harness; RQ4 placement | L3 classical; tuning documentation; bias/variance statistics | Producto de difúsión; all figures; repo |

**Rules:**
- **A pairs with B in weeks 3–4.** B is otherwise a single point of failure for the core method; if the PINN stalls there is no project.
- **C owns the interface.** All methods return the same result object; everything config-driven; nothing merges that cannot regenerate a figure.
- Build the seed loop and logging in **week 5, before the main sweep.** Retrofitting means rerunning everything.
- **Week 8 splits the team:** C takes the *producto de difusión* while A and B finish the real-data arm and diagnostics. Agree this split in week 1, not week 8.
- Weeks 9–11 are shared: everyone writes.

### 4.12 Timeline, course deliverables and gates

The programme runs **11 weeks** with a fixed deliverable each week. Those deliverables are a *reporting cadence*, not a work plan — work starts when the dependency clears, not when the report is due. Two rules follow: B starts the PINN in week 3 even though "modelos alternativos" is not due until week 6, and week 2 carries real engineering because the convenio is a signature, not a workload.

#### Deliverable mapping

| Semana | Entregable de referencia | Entregable comprometido | Gates closed |
|---|---|---|---|
| 1 | Planteamiento del proyecto | **Planteamiento del proyecto** *(obligatorio)* | — |
| 2 | Avance 0. Propuesta y firma de convenios | **Avance 0 + verificación de datos y solver de referencia** | **G0, G1** |
| 3 | Avance 1. Análisis exploratorio de datos | **Avance 1. Análisis exploratorio de mediciones publicadas (NIST SP 260-177)** | **G2** |
| 4 | Avance 2. Ingeniería de características | **Avance 2. Adimensionalización, formulación mixta y diseño de la configuración de medición** | **G3** |
| 5 | Avance 3. Baseline | **Avance 3. Baseline — extracción estandarizada SEMI MS4, inversión clásica y posteriores MCMC de referencia (L0)** | **G4** |
| 6 | Avance 4. Modelos alternativos | **Avance 4. Modelos alternativos — flexibilidad implícita (L1) y discrepancia explícita (L2)** | — |
| 7 | Avance 5. Modelo final | **Avance 5. Modelo final — discrepancia estructurada (L3) y escalera completa L0–L3** | **G5** |
| 8 | Avance 6. Producto de difusión | **Avance 6. Producto de difusión** *(obligatorio)* + brazo de datos reales | **G6 — hard stop** |
| 9 | Avance 7. Resumen ejecutivo | **Avance 7. Resumen ejecutivo** *(obligatorio)* | — |
| 10–11 | Presentación final | **Presentación final** *(obligatorio)* | — |

**Justification for the three adapted deliverables** — required by the course, so write it once and reuse it:

- **Week 3 (EDA).** The dataset is NIST's published measurement tables rather than a conventional ML corpus, but the work is genuine exploratory analysis: distribution of extracted modulus across twelve cantilevers, between-lab reproducibility spread, uncertainty-budget structure, and the length-drift signature. **The A8 drift test *is* the exploratory finding that defines the research question.**
- **Week 4 (feature engineering).** Features here are the measurement configuration, not table columns. Non-dimensionalization is feature scaling — without it, loss terms span 10+ orders of magnitude and nothing trains. Sensor placement is feature selection: which points along the beam, how many, how many modes. RQ4 lands here.
- **Weeks 5–7.** No adaptation needed. L0 is literally the baseline (an international standard test method, so it cannot be called a strawman), L1/L2 are literally the alternative models, L3 plus the full comparison is literally the final model.

**Open question for the supervisor (§3.4, Q3):** is the final presentation the last deliverable, or is a separate written thesis also due? If a thesis document is required, confirm its deadline in week 1 — it changes the scope cuts below.

#### Week-by-week tasks

**Week 1 — Planteamiento**
- [all] Draft the planteamiento from §3 and §4.2
- [all] Supervisor conversation, three questions of §3.4, **answers recorded in writing**
- [all] Agree the week-8 split now: who takes the *producto de difusión*
- [B/C] Read Zou et al. 2024 and Brynjarsdóttir & O'Hagan 2014; **write the differentiating paragraph**
- [C] Read arXiv:2509.20191 body text; correct or confirm A5's secondary claims
- [C] Repo skeleton, branch policy, result-object interface stub

**Week 2 — Avance 0 + verification (G0, G1)**
- [all] Full §5.4 checklist: NIST E-vs-length, Figs. RS10/SG10, trace digitizability, table transcription to CSV
- [C] Reproduce one MEMS Calculator data-analysis sheet end to end — this *is* Method 1
- [A] Eigensolver (finite-difference or Rayleigh–Ritz, `scipy.linalg.eigh`)
- [A] Validate against analytical roots 1.875 / 4.694 / 7.855; pytest regression tests
- [all] **Decision recorded:** both arms / one arm / pivot to squeeze-film (§3.1.2)
- **G0:** at least one real-data arm usable; differentiator written. Both arms fail → pivot, not synthetic-only.
- **G1:** frequencies correct to <0.1% vs analytical. Fail → Tier 0.

**Week 3 — Avance 1, EDA (G2)**
- [A] M0–M3 generators; **check spring sign conventions** — a sign error silently flips the severity axis
- [A] Severity calibration so one M1 point lands at ≈5% systematic
- [C] Misfit surface over E, σ₀, k_θ; identifiability check
- [C] EDA write-up: modulus distributions, round-robin spread, uncertainty budget, length drift
- [B] **Start the PINN now**, paired with A — do not wait for week 6
- **G2:** E and σ₀ separable via cantilever + bridge; k_θ separable via modes 1–3. Fail → recover E only.

**Week 4 — Avance 2, feature engineering (G3)**
- [A] Non-dimensionalization, fully documented — ξ = x/L, W = w/h, grouped constants
- [B] Mixed-form PINN: two outputs (w, M), two second-order residuals. **Never `w''''`.**
- [B] Validate PINN against the reference to <1%; hard vs. soft BC ablation
- [B] **Time a single run.** >1 min → trigger the §4.8 cut order immediately
- [C] Fisher-information sensor placement analysis — **RQ4 finishes here**
- **G3:** PINN matches reference <1%; run time known and cut order triggered if needed.

**Week 5 — Avance 3, baseline (G4)**
- [C] Classical nested inverse (`least_squares` around the eigensolver)
- [C] **Config/seed/W&B harness live before any sweep runs.** Retrofitting means rerunning everything.
- [A] Both MCMC posteriors: P_simple (L0 model) and P_rich (L3 model)
- [A] ArviZ diagnostics, R̂ < 1.01, ESS reported
- [B] L0 PINN at fixed high λ_PDE
- [all] **Draft the methods section and write the abstract both ways.** Week 5, not week 9.
- **G4:** all L0 methods recover known parameters under M0 noiseless; both posteriors converge.

**Week 6 — Avance 4, alternative models**
- [B] L1 sweep: relaxed λ_PDE across the M1 severity axis
- [B] L1 adaptive/learned λ_PDE — **RQ3**
- [B] L2: PINN + discrepancy network δ(ξ)
- [A] L2 classical: LSQ + smooth discrepancy basis
- [C] Baseline tuning paragraphs, one per method, written as they run
- [C] Bias/variance statistics pipeline against both posteriors

**Week 7 — Avance 5, final model (G5)**
- [C] L3 classical: k_θ and k_u as extra unknowns
- [B] L3 in-network: k_θ and k_u as trainable scalars
- [all] Complete L0–L3 × M1 degradation curves
- [A] M2 (Timoshenko) and M3 (taper) single-point generalization checks
- **G5:** core ladder sweep complete. Fail → stop, present L0/L1 + partial (Tier 1).

**Week 8 — Avance 6, difusión + real data (G6)**
- [C] **Producto de difusión**: poster/repo/whatever the course requires. README must regenerate every figure from configs.
- [A] Arm 1 — ladder on cantilever frequency data; fit `(L/(L+ΔL))⁴`; report ΔL with a confidence interval
- [A] Arm 2 — ladder on shape traces; cross-check that both arms imply the same ΔL
- [B] Residual diagnostics: does L1's flexibility hide the misspecification symptom?
- [C] All figures final — median + IQR on every plot
- **G6: HARD STOP on all experiments. No exceptions.**

**Week 9 — Avance 7, executive summary**
- [all] Executive summary
- [all] Limitations section drawn from the decision log — far more convincing written contemporaneously
- [C] Repo cleanup, README, reproducibility check from a clean clone

**Weeks 10–11 — Final presentation**
- [all] Build and rehearse the presentation
- [all] Prepare for the two questions that will come: *why not high dimensions or design?* (§3.1.1) and *isn't this already in Zou et al.?* (§3.1.2, §2.3)

#### Scope consequences of the 11-week calendar

Freeing week 2 from convenio paperwork restores roughly the week the shorter calendar cost. Relative to a 13-week plan:

| Kept | Cut |
|---|---|
| Full L0–L3 ladder | FEniCSx anchor model (cite Kobrinsky instead) |
| Both MCMC posteriors | Field inversion σ₀(x) (Tier 4) |
| 10 seeds, median + IQR | Dense M2/M3 sweeps — single points only |
| RQ4 sensor placement (lands week 4) | Arm 2 if traces do not digitize cleanly at G0 |
| Real-data Arm 1 | — |

**Week 4 is the tightest week** — non-dimensionalization, a validated mixed-form PINN, the timing measurement and the placement analysis all land together. This is exactly why B starts in week 3.

### 4.13 Fallback tiers

Every tier is independently defensible. Present **Tier 3 as the project**; Tier 4 is the extension.

| Tier | Content | Trigger |
|---|---|---|
| **Tier 0** | Cantilever, recover E only, M0 only, swept over N and noise | G1 or G2 fails |
| **Tier 1** | Scalar E and σ₀, both structures, M0 + M1, **L0 vs L1 only** | G5 fails |
| **Tier 2** | Above + L2 and L3 + both reference posteriors | — |
| **Tier 3 (target)** | Above + **real-data arm (RQ5)** + placement (RQ4) + M2/M3 checks | — |
| **Tier 4 (extension)** | Above + field σ₀(x) vs Tikhonov; dense M2/M3 sweeps; FEniCSx-derived springs | Out of scope on the 11-week calendar; future work |

**Note the change from v2:** the real-data arm is now *inside* the target tier. v2 put it in Tier 4 while simultaneously calling it the difference between a controlled study and a validated one. It cannot be both optional and decisive.

### 4.14 Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Zou et al. 2024 is closer than expected; novelty collapses** | Medium | Week-1 read and written differentiator. We characterize the ladder their method sits on; they propose one rung of it. If genuinely overlapping, pivot emphasis to L3 + RQ5, which they do not cover. |
| **The KOH literature makes H3 look like a known result** | Medium | It *is* a known result in general form. Frame H3 as a prediction being tested in a new regime, and make L1 — which KOH does not contain — the novel object. |
| PINN run time > 1 min, matrix collapses | Medium | G3 timing gate; pre-agreed cut order in §4.8. Mixed formulation is the main defence. |
| Real data is derived scalars only, not mode shapes | **High** | Already assumed (A9). Arm 1 runs weakly supervised on one frequency per structure, and the length sweep *is* the A8 test. **Arm 2 is unaffected** — the strain structures carry dense spatial traces regardless (§4.10). This is the main reason the real-data arm was split in two. |
| **G0 fails outright: NIST data unusable for both arms** | Low–Medium | **Pivot to squeeze-film damping in the rarefied regime (§3.1.2), not to a synthetic-only study.** Ladder, both posteriors, harness and analysis code all transfer. Accept the weaker incumbent and say so in the limitations. Decide in week 1, never later. |
| NIST E-vs-length shows no drift | Medium | Report the null with a confidence interval on ΔL — a bounded anchor compliance is itself a result. Cross-check against Arm 2 (Figs. RS10/SG10) before concluding, and fall back on the round-robin spread as the real-data signal. |
| **L3 wins everywhere and the PINN adds nothing** | **High** | Framed as the expected result (A7). "Knowing the error's form beats every generic treatment, including network flexibility, at 40× lower cost" is a finding. Supervisor agreement secured week 1. |
| k_θ not identifiable from available data | Medium | Week-2 gate; higher modes are the handle. Fail → fix k_θ from FEniCSx or Kobrinsky and fit k_u only. |
| PINN training unstable at high severity | Medium | Report the instability as a result, consistent with A2. |
| Three incompatible codebases | **High** | C owns the interface. Config-driven from week 4. |
| Writing compressed | Medium *(was High)* | G6 at week 8 is an unconditional stop; methods drafted week 5; weeks 9–11 are writing and presentation only. |
| Scope creep back toward MEMS device detail | Medium | Beam equation, measurement context, one motivation section. Nothing more. |

### 4.15 Deliverables

1. **Thesis document** — the ladder study as the core, M0 as the warm-up chapter, real-data arm as validation.
2. **Reproducible repository** — config-driven, seeded, README that regenerates every figure from scratch.
3. **Experiment log** — every run tracked, including failures.
4. **Decision log** — which tier, and why, recorded *at the time*. This becomes the limitations section and is far more convincing written contemporaneously than reconstructed at the end.

### 4.16 What will actually determine the grade

1. Seed discipline — 10 seeds, median and IQR on every plot, from day one.
2. Tuned baselines with documented tuning effort. L0 must be the real standard, not a cartoon.
3. **Bias separated from variance, and estimator bias separated from model-form bias.** This is RQ2; collapsing any of it into RMSE destroys the finding.
4. A one-paragraph differentiation from Zou et al. and from Brynjarsdóttir & O'Hagan, in the introduction, written in week 1.
5. Honest negative results — "undeclared flexibility is worse than doing nothing above 3% model error" is a good conclusion.
6. Reproducibility — a repo that regenerates figures from configs.
7. The real-data chapter with the A8 curve fit. It is the difference between a controlled study and a validated one.

---

## 5. Data sources

### 5.1 Primary — free, immediate

**NIST Special Publication 260-177**, *Standard Reference Materials: User's Guide for RM 8096 and 8097: The MEMS 5-in-1, 2013 Edition*. Cassard, Geist, Vorburger, Read, Gaitan & Seiler. 253 pages.
DOI: 10.6028/NIST.SP.260-177 — free PDF at `https://www.nist.gov/system/files/documents/srm/SP260-177.pdf`

| Content | Location | Use |
|---|---|---|
| **Young's modulus vs. cantilever length** | **YM tables/figures — locate at G0, week 2** | **The A8 test. Highest-priority item in the document.** |
| Young's modulus repeatability — one lab, one instrument, twelve cantilevers | Table YM7 | Real within-lab spread |
| Young's modulus reproducibility — eight participants, five labs, seven instruments, four chips | Table YM8, Fig. YM6 | Uncertainty floor; the bar for H4 |
| Cantilever specifications for Young's modulus | Table YM1 | Geometry inputs |
| Fixed-fixed beam configurations | Table RS1 | Geometry inputs |
| Residual strain vs. length | Fig. RS10, Table RS9 | Secondary A8 signature |
| Strain gradient vs. length | Fig. SG10, Table SG8 | Secondary A8 signature |
| **2D data traces along beams** | **Figs. RS2(c), RS3(c), SG2(c), SG3(c)** | **Arm 2's primary data — the only dense spatial measurements available. Check digitizability at G0, week 2.** |
| Full uncertainty budgets incl. σ_support, σ_cantilever | §2.4, §3.4, §4.4 | Grounds A4; supplies severity calibration |
| Reproductions of the data analysis sheets | Appendices 1–7 | The standardized algorithm, step by step |

Test methods referenced: **SEMI MS4** (Young's modulus from cantilever resonance — *this is the modality*), **ASTM E 2245** (residual strain), **ASTM E 2246** (strain gradient), **SEMI MS2** (step height), **ASTM E 2244** (in-plane length).

**NIST MEMS Calculator — SRD 166.** Free online implementation of the standardized extraction, via the NIST Data Gateway (`http://srdata.nist.gov/gateway/`, keyword "MEMS Calculator"). This is **Method 1**.

### 5.2 Secondary — published tables

| Source | Content | Notes |
|---|---|---|
| Kobrinsky, Deutsch & Senturia (2000), *JMEMS* 9(3), 361–369 | Support compliance effects; length-dependent deflection at constant stress | **Grounds M1, supplies k values, and is the template for A8** |
| Gupta / Senturia step-by-step procedure | Polysilicon E across three support post designs; systematic error assessment | Severity calibration target (A4) — **verify the exact figures against the source** |
| Osterberg & Senturia (1997), *JMEMS* 6(2), 107–118 | M-TEST | Cite as precedent; dataset ruled out |
| Ochoa et al. (2022), *Micromachines* | LPCVD Si₃N₄, thickness-dependent modulus | Open access; Universidad de Guanajuato co-author — local contact worth an email |

### 5.3 Ruled out

| Source | Why |
|---|---|
| Buying RM 8096 / 8097 chips | ~$1–2k, and you'd still need a vibrometer |
| Pull-in voltage datasets | Limit point; needs pseudo-arclength continuation |
| Buckled fixed-fixed beam shape data | Bifurcation; two stable states (Kobrinsky). Same objection as pull-in. |
| Static deflection data | **E cancels out.** See §1, change 2. |
| Fabricating anything | No fab access, no time |

### 5.4 Week-2 verification checklist (G0)

**Arm 1 — frequency**
- [ ] Download SP 260-177. **Locate apparent-E versus cantilever length. Is there drift, and does it fit `(L/(L+ΔL))⁴`?**
- [ ] Transcribe Tables YM1, YM7, YM8 into CSV.
- [ ] Confirm mode-shape or multi-mode frequency data availability. If only ω₁ exists, Arm 1 runs weakly supervised and L3 identifiability rests on the length sweep — flag at G2.

**Arm 2 — shape**
- [ ] Open Figs. RS2(c), RS3(c), SG2(c), SG3(c). **Are the traces digitizable at usable density?** This is what decides whether Arm 2 carries spatial residual diagnostics.
- [ ] Open Figs. RS10 and SG10. Does apparent strain or strain gradient drift with length, and is the implied ΔL consistent with Arm 1's?
- [ ] Transcribe Tables RS1, RS9, SG1, SG8 into CSV.

**Both**
- [ ] Open the MEMS Calculator; reproduce one NIST data analysis sheet end-to-end.
- [ ] Read Zou et al. (2024) and Brynjarsdóttir & O'Hagan (2014). Write the differentiating paragraph.
- [ ] Read arXiv:2509.20191 body text; correct or confirm A5's secondary claims.
- [ ] Supervisor conversation (§3.4), answers recorded in writing.

**Decision at the end of week 1, in writing:** both arms viable → proceed as planned. One arm viable → proceed with that one and note the loss. **Neither arm viable → pivot to squeeze-film (§3.1.2) immediately**, not to a synthetic-only study.

---

## 6. Software, tooling and resources

### 6.1 Critical path — all free

| Tool | Role |
|---|---|
| **Python 3.11+** | Everything |
| **NumPy / SciPy** | `scipy.linalg.eigh` (generalized eigensolver — the reference), `optimize.least_squares` (classical inverse), `interpolate` |
| **PyTorch** | PINN backend |
| **DeepXDE** | Fastest path to a working PINN; supports trainable physical parameters and hard BC transforms. **Verify it supports multi-output mixed formulations cleanly before committing — if not, drop to raw PyTorch in week 3, not week 6.** |
| **emcee** or **PyMC** | Both reference posteriors |
| **ArviZ** | R̂ and ESS — needed for the tuning-documentation paragraph |
| **Weights & Biases** | Sweeps, seed tracking, failure logging (free academic tier) |
| **Hydra** or plain YAML | Config-driven runs; C owns this |
| **pytest** | Regression tests on the eigensolver — cheap insurance for G1 |
| **matplotlib** | Figures; median + IQR on everything |
| **Git / GitHub** | Repo with a README that regenerates every figure |

### 6.2 Off the critical path — optional, free

| Tool | Role |
|---|---|
| **FEniCSx** or **Elmer** + **Gmsh** | One 2D plane-stress anchor model to derive k_θ and k_u (§4.5) |
| **JAX** | Cleaner high-order derivatives — rejected; the mixed formulation removes the need |

### 6.3 Ruled out

| Tool | Why |
|---|---|
| **COMSOL + MEMS Module** | No individual student version. If a university network licence exists, validation appendix only. |
| **ANSYS Student** | 128K node cap and no electromagnetics. Not needed under current scope. |
| **NVIDIA PhysicsNeMo** | Overkill for a 1D problem |
| **Operator learning (DeepONet, FNO)** | Requires a large generated training set |

### 6.4 Compute

The problem is small. CPU suffices; a single consumer GPU or Colab is a bonus. Three people on three machines is the intended parallelism — another reason the config-driven harness must exist before week 5.

---

## Appendix A: governing equations

**Inversion model — Euler–Bernoulli free vibration with axial load:**
```
E·I·w'''' − N·w'' − ω²ρA·w = 0,    N = σ₀·b·h,    I = b·h³/12,    A = b·h
```
with ω supplied as measured data.

**Mixed form used by the PINN (two outputs, two second-order residuals):**
```
r₁ :  M − E·I·w''            = 0
r₂ :  M'' − N·w'' − ω²ρA·w   = 0
```

**M1 generator — compliant supports (rotational and translational):**
```
M(0) = k_θ · w'(0)        M(L) = −k_θ · w'(L)
V(0) = k_u · w(0)         V(L) = −k_u · w(L)
```
replacing ideal clamped conditions. As k_θ, k_u → ∞ the ideal case is recovered. **Check the moment and shear sign conventions against the eigensolver in week 2** — a sign error here silently inverts the severity axis.

Equivalent effective-length parameterization used for A8:
```
E_app / E_true  ≈  (L / (L + ΔL))⁴
```

**M2 generator — Timoshenko (shear deformation + rotary inertia):**
Two coupled first-order-in-rotation equations; shear coefficient κ_s and G = E/2(1+ν). Matters for small L/h and for higher modes.

**M3 generator — linear thickness taper:**
```
h(ξ) = h₀(1 + α·ξ)   →   I(ξ) = b·h(ξ)³/12,   A(ξ) = b·h(ξ)
```

**Analytical checks (G1):**
- Cantilever roots: `βL = 1.875, 4.694, 7.855`; `f₁ = (1.875²/2π)·√(EI / ρAL⁴)`
- Clamped–clamped roots: `βL = 4.730, 7.853, 10.996`
- Axial-load limit: as N → tensile, f₁ increases monotonically; as N → −P_cr, f₁ → 0. **Use this as the sub-critical guard.**
- Compliance limit: as k_θ → 0 the cantilever root → pinned-free value. Test both ends of the sweep.

**Deliberately excluded:** electrostatic loading and pull-in (limit point); buckled-beam shape (bifurcation, two stable states); static deflection (E cancels).

---

## Appendix B: discarded options and why

| Option | Why discarded |
|---|---|
| Pure forward-problem PINN vs FEM | Indefensible framing; FEM wins on accuracy and time (A1) |
| PINN vs classical inverse, correct model, noise only | **Done, published, and PINNs lose** — arXiv:2509.20191 (A5) |
| Plain "PINN as design surrogate" | A GP on a few hundred FEM runs likely wins on accuracy, time, and gives free UQ |
| Static deflection modality | **E cancels out** of both the cantilever arc and the buckling condition |
| Buckled fixed-fixed beam shape | Bifurcation with two stable states; same objection used to rule out pull-in |
| Pull-in / bifurcation data | Limit point; would need pseudo-arclength continuation |
| Mid-plane stretching as M2 | Large-amplitude static effect; meaningless in a small-amplitude modal measurement |
| Field inversion σ₀(x) + Tikhonov (v2 RQ3) | A second project; crowded (Teloli et al.); deleting it buys the writing weeks. Tier 4. |
| Squeeze-film damping in the rarefied regime | **Not discarded — held in reserve as the G0 fallback (§3.1.2).** Genuinely competitive, and its three competing slip corrections would upgrade L3 to model selection. Loses the standardized incumbent and the round-robin data, which is why it is second choice rather than first. |
| High-dimensional PDEs (filtering, control) | No reference solution exists in that regime, so no ground truth, no error metric, no defensible claim (§3.1.1) |
| Complex-geometry showcase | Real competitors are cut-cell FEM, meshfree and IGA; advantage is setup effort, not accuracy; needs CAD + meshing + a FEM reference we do not have (§3.1.1) |
| Design surrogacy / parametric PINN | A GP on a few hundred FEM runs likely wins and gives free UQ; generating those runs needs the licensed FEM we lack; no incumbent and no real data (§3.1.1) |
| PMUT surrogate | Piezo constitutive equations *and* PINN debugging is two hard things at once |
| Gyroscope mode matching | Needs careful 3D modal FEM; licence risk |
| Operator learning (DeepONet, FNO) | Requires a large generated training set |
| Contact and stiction | Non-smooth; fragile in every method |
| Inverse-crime-only synthetic study (v1) | Both methods hold the exactly correct model; removes the one condition of interest |

---

## Appendix C: references

*Verify every entry against the publisher of record before submission, and check the required citation style for the programme. Entries marked ✔ were checked against the publisher during planning.*

**Model discrepancy — the theoretical spine (new in v3)**
1. Kennedy, M.C. & O'Hagan, A. (2001). Bayesian calibration of computer models. *J. R. Stat. Soc. B*, 63(3), 425–464. *(The origin of explicit discrepancy modelling — L2.)*
2. Brynjarsdóttir, J. & O'Hagan, A. (2014). Learning about physical parameters: the importance of model discrepancy. *Inverse Problems*, 30(11), 114007. *(Bias persists under explicit discrepancy unless its form is known — the basis of H3.)*
3. Zou, Z., Meng, X. & Karniadakis, G.E. (2024). Correcting model misspecification in physics-informed neural networks (PINNs). *J. Comput. Phys.*, 505, 112918. ✔ **← closest neighbour; this is L2; differentiate in week 1 (A6)**
4. Kaipio, J. & Somersalo, E. (2005). *Statistical and Computational Inverse Problems*. Springer. *(For the precise definition of inverse crime — note it refers to shared discretization, not merely shared model.)*

**PINN foundations and critique**
5. Raissi, M., Perdikaris, P. & Karniadakis, G.E. (2019). Physics-informed neural networks. *J. Comput. Phys.*, 378, 686–707.
6. Grossmann, T.G., Komorowska, U.J., Latz, J. & Schönlieb, C.-B. (2024). Can physics-informed neural networks beat the finite element method? *IMA J. Appl. Math.*, 89(1), 143–174. ✔ DOI 10.1093/imamat/hxae011
7. Krishnapriyan, A., Gholami, A., Zhe, S., Kirby, R. & Mahoney, M.W. (2021). Characterizing possible failure modes in physics-informed neural networks. *NeurIPS*, 34.
8. McGreivy, N. & Hakim, A. (2024). Weak baselines and reporting biases lead to overoptimism in machine learning for fluid-related PDEs. *Nature Machine Intelligence*.
9. Jekic, A. et al. (2025). Examining the robustness of physics-informed neural networks to noise for inverse problems. arXiv:2509.20191. ✔ *(NTNU/SINTEF; Burgers and Navier–Stokes; classical approach wins.)*
10. Wang, S., Teng, Y. & Perdikaris, P. (2021). Understanding and mitigating gradient flow pathologies in PINNs. *SIAM J. Sci. Comput.*, 43(5), A3055–A3081. *(Adaptive weighting — RQ3.)*
11. Wang, S., Yu, X. & Perdikaris, P. (2022). When and why PINNs fail to train: a neural tangent kernel perspective. *J. Comput. Phys.*, 449, 110768.
12. Yang, L., Meng, X. & Karniadakis, G.E. (2021). B-PINNs: Bayesian physics-informed neural networks. *J. Comput. Phys.*, 425, 109913.
13. Lu, L., Pestourie, R., Yao, W., Wang, Z., Verdugo, F. & Johnson, S.G. (2021). PINNs with hard constraints for inverse design. *SIAM J. Sci. Comput.*, 43(6), B1105–B1132.
14. Amini, D., Haghighat, E. & Juanes, R. (2022). PINN solution of thermo–hydro–mechanical processes in porous media. *J. Eng. Mech.*, 148(11), 04022070. *(Non-dimensionalization; sequential and adaptive weighting.)*
15. Lu, L., Meng, X., Mao, Z. & Karniadakis, G.E. (2021). DeepXDE. *SIAM Review*, 63(1), 208–228.
16. Teloli, R., Tittarelli, R., Bigot, M., Coelho, L., Ramasso, E., Le Moal, P. & Ouisse, M. (2024/2025). PINN framework for model parameter identification of beam-like structures / localized assessment in Euler–Bernoulli beams. *(Nearest prior art on the beam equation itself, including spatially varying properties — the reason v2's RQ3 was deleted.)*

**MEMS measurement and the misspecification**
17. Cassard, J.M., Geist, J., Vorburger, T.V., Read, D.T., Gaitan, M. & Seiler, D.G. (2013). *User's Guide for RM 8096 and 8097: The MEMS 5-in-1*. NIST SP 260-177. DOI 10.6028/NIST.SP.260-177.
18. Kobrinsky, M.J., Deutsch, E.R. & Senturia, S.D. (2000). Effect of support compliance and residual stress on the shape of doubly supported surface-micromachined beams. *J. Microelectromech. Syst.*, 9(3), 361–369. ✔ **← grounds M1 and A8**
19. Osterberg, P.M. & Senturia, S.D. (1997). M-TEST. *J. Microelectromech. Syst.*, 6(2), 107–118.
20. SEMI MS4 — Young's modulus from the frequency of beams in resonance. *(The modality.)*
21. ASTM E 2245 — residual strain from fixed-fixed beams.
22. ASTM E 2246 — strain gradient from cantilevers.
23. NIST Standard Reference Database 166 — MEMS Calculator.
24. Senturia, S.D. (2001). *Microsystem Design*. Kluwer.
25. Ochoa, L. et al. (2022). Estimation of the Young's modulus of nanometer-thick films using residual stress-driven bilayer cantilevers. *Micromachines*. *(Verify full citation; local Guanajuato co-author.)*

---

*v3. Update the decision log as gates fire. G0 comes before everything else, and G6 at week 8 is unconditional.*
