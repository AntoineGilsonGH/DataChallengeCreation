# Motivation of our Data Challenge

## Why snow depth forecasting?

Snow depth prediction is a concrete, high-stakes problem at the intersection of
climate science, hydrology, and machine learning. Accurate short-term snowpack
forecasts have direct applications in:

- **Winter sports and infrastructure** — ski resorts, avalanche risk assessment,
  road safety in mountain passes
- **Water resource management** — snowmelt is a primary source of river flow in
  Alpine watersheds, critical for agriculture and hydropower
- **Climate monitoring** — snowpack is one of the most sensitive indicators of
  climate change in mountain regions

The 2030 Winter Olympics in the French Alps provide a concrete and timely anchor
for the challenge, but the underlying problem is relevant well beyond the event.

## Why this dataset?

Météo-France's SIM model is a state-of-the-art public hydrometeorological reanalysis
that combines atmospheric observations with a physically-based snow model. It
provides a rare combination of: physical consistency, spatial coverage and temporal depth 

This makes it a genuinely interesting regression problem where simple baselines
work reasonably well (~0.12m RMSE with a Random Forest) but where there is clear
room for improvement through better feature engineering, spatial modeling, or maybe
physically-informed approaches.

## Specific challenges

**Temporal structure** — the data has strong autocorrelation. A model that
ignores the time dimension and treats each row independently will leave
significant performance on the table. Participants are encouraged to think about
how to exploit past observations.

**Spatial structure** — nearby grid points share similar weather but differ in
altitude and exposure. LAMBX and LAMBY encode position but not altitude directly,
which creates an interesting feature engineering challenge.

**Class imbalance analog** — a large fraction of grid points have near-zero
snow depth, particularly at lower altitudes and at the start/end of the season.
Models that minimize average RMSE may implicitly focus on these easy cases.
The most interesting predictions are for high-altitude, high-snowpack situations.

**Climate trend** — the 2020-2026 period spans a warming trend. A model trained
on 2020-2024 and tested on 2025-2026 may face a mild distribution shift, which
is realistic and intentional.

## Limitations

We are transparent about the constraints of this challenge:

- **Short time range** — 6 years of data is modest for a temporal problem. A
  richer dataset would go back to 1990, but was excluded here to limit
  computational cost and keep the challenge accessible.
- **No altitude variable** — the SIM grid does not directly provide elevation.
  It is implicitly encoded in the snow variables but not explicitly available,
  which limits certain physically-motivated approaches.
(Pyrenees, Vosges) and limits the geographic
  generalization of models.
- **Single horizon** — only J+7 is evaluated. Multi-horizon forecasting (J+1
  through J+14) would be more useful operationally but adds complexity.

These limitations are mostly deliberate tradeoffs in favor of accessibility and focus,
not oversights.