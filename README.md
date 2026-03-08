# Alpine Snow Depth Forecasting — French Alps 🏔️

> *Can machine learning predict snow depth in the French Alps?*

## Context

The French Alps will host the **2030 Winter Olympics**. In a context of accelerating
climate change, snow conditions in mountain regions are increasingly uncertain.
This challenge asks you to predict **snow depth 7 days ahead** across the French
Alps, using daily meteorological observations from Météo-France's SIM model.

## Task

**Regression** — predict `HTEURNEIGE_J7`: snow depth (in meters) at day J+7,
for each Alpine grid point, given meteorological observations at day J.

- **Baseline RMSE**: ~0.12m (Random Forest, see `solution/submission.py`)
- **Metric**: RMSE (primary), MAE (secondary)

## Data

Data comes from **Météo-France's SIM model** (Système d'Information de la Montagne),
a hydrometeorological reanalysis at **8km resolution** covering France.

### Download

| File | Description | Size |
|---|---|---|
| [X_train.csv](#) | Training features (winters 2020→2024) | ~70MB |
| [y_train.csv](#) | Training labels — HTEURNEIGE_J7 | ~20MB |

> ⚠️ `X_test.csv` is not provided — it is used server-side by Codabench for evaluation only.

### Preprocessing applied

The raw SIM dataset covers all of France at 8km resolution with 29 meteorological
variables. The following preprocessing was applied to create the challenge dataset:

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

Variables that directly encode the snow state at J+7 (e.g. `HTEURNEIGE6`,
`HTEURNEIGEX`, `RESR_NEIGE6`) were excluded to prevent data leakage.
Only variables reflecting the state of the snowpack **at day J** are provided
as features, alongside atmospheric forcing variables.

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

## Repository structure

```
├── competition.yaml              # Codabench competition config
├── ingestion_program/
│   └── ingestion.py              # Loads data, calls get_model(), saves predictions
├── scoring_program/
│   └── scoring.py                # Computes RMSE and MAE from predictions
├── solution/
│   └── submission.py             # Baseline Random Forest — submit this as a starting point
├── pages/                        # Markdown pages displayed on Codabench
├── dev_phase/                    # Data for development phase (public test)
│   ├── input_data/
│   │   ├── X_train.csv
│   │   ├── y_train.csv
│   │   ├── test/X_test.csv
│   │   └── private_test/X_test.csv
│   └── reference_data/
│       ├── test_labels.csv
│       └── private_test_labels.csv
└── tools/
    ├── create_bundle.py          # Creates bundle.zip for Codabench upload
    └── Dockerfile                # Docker image used by Codabench
```

## Local testing

```bash
# Test ingestion
python ingestion_program/ingestion.py \
  --data-dir dev_phase/input_data/ \
  --output-dir ingestion_res/ \
  --submission-dir solution/

# Test scoring
python scoring_program/scoring.py \
  --reference-dir dev_phase/reference_data/ \
  --prediction-dir ingestion_res/ \
  --output-dir scoring_res/

# Check scores
cat scoring_res/scores.json

# Create bundle
python tools/create_bundle.py
```

## Submit to Codabench

1. Implement your model in `submission.py` following the structure in `solution/submission.py`
2. Create a zip: `zip submission.zip submission.py`
3. Upload on [Codabench](https://www.codabench.org)
