# Alpine Snow Depth Forecasting — French Alps 🏔️

> *Can machine learning predict snow depth in the French Alps?*

## Context

The French Alps will host the **2030 Winter Olympics**. In a context of accelerating
climate change, snow conditions in mountain regions are increasingly uncertain.
This challenge asks you to predict **snow depth 7 days ahead** across the French
Alps, using daily meteorological observations from Météo-France's SIM model.

## Task

The task you will have to perform is a **Regression**, and more particularly regress the target variable `HTEURNEIGE_J7`: **snow depth (in meters) at day J+7**,
for each Alpine grid point, given meteorological observations at day J.

## Data
Data comes from **Météo-France's SIM model** (Système d'Information de la Montagne),
a hydrometeorological reanalysis at **8km resolution** covering France.
It can be accessed at [meteo.data.gouv.fr](https://meteo.data.gouv.fr/datasets/6569b27598256cc583c917a7).

### Preprocessing applied to Météo-France's SIM Data for the challenge

The raw SIM dataset covers all of France at 8km resolution with 29 meteorological
variables, on a daily basis since 1960. This makes the whole data really heavy to handle. To keep this challenge accessible and focused on modeling quality rather than computational power, several deliberate choices were made to limit the size and complexity of the dataset. The following preprocessing was applied to create the challenge dataset:

**1. Geographic filtering — French Alps only**

The full France dataset (~22M rows/year) was filtered to the French Alps bounding
box in Lambert II étendu coordinates:
```
LAMBX ∈ [8000, 11000] hm
LAMBY ∈ [19000, 21500] hm
```
This corresponds to the Savoie, Haute-Savoie, Isère and Hautes-Alpes departments.

**2. Altitude filtering**

Grid points that never recorded any snow (`HTEURNEIGE == 0` across all records)
were removed. This eliminates low-altitude valley points that are not relevant
to the challenge, reducing noise and computational cost.

**3. Seasonal filtering — winter only**

Only winter months (October → April) are kept. Summer months contribute no
snow signal and would inflate the dataset with trivial zero-snow predictions.

**4. Feature selection — leakage prevention**

Variables that might directly encode the snow state at J+7 or were too correlated to other variables (e.g. `HTEURNEIGE6`,
`HTEURNEIGEX`, `RESR_NEIGE6`) were excluded to prevent data leakage.

**5. Target construction**

The target `HTEURNEIGE_J7` is constructed by shifting `HTEURNEIGE` by 7 days
within each grid point, using a temporal groupby to avoid cross-point leakage
at season boundaries.

### Result

| | Value |
|---|---|
| Grid points (Alps, snow only) | **722** |
| Train rows | **~1.2M** |
| Public test rows | **~200k** (winter 2024-2025) |
| Private test rows | **~200k** (winter 2025-2026) |


# Download / The data is available here by downloading in Get Started/Files/Input_Data