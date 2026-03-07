# How to Participate

## Reminder of the context

The French Alps will host the 2030 Winter Olympics. In a context of accelerating
climate change, snow conditions in mountain regions are increasingly uncertain.
This challenge asks you to predict **snow depth 7 days ahead** across the French
Alps, using daily meteorological data from Météo-France's SIM model.

## Your submission

You must submit a Python file named `submission.py` containing a `get_model()`
function that returns a scikit-learn compatible model. This model will be:

1. **Trained** on historical data (winters 2020 → 2024) by calling `model.fit(X_train, y_train)`
2. **Evaluated** on unseen winter seasons by calling `model.predict(X_test)`

See the **Seed** page for the expected structure of your `submission.py`.

## Input data

Your model receives the following features at day J for each Alpine grid point:

| Feature | Description | Unit |
|---|---|---|
| LAMBX, LAMBY | Grid point position (Lambert II) | hm |
| DATE | Date of observation | datetime |
| T, TINF_H, TSUP_H | Mean, min, max daily temperature | °C |
| PRENEI | Solid precipitation (snow accumulation) | mm |
| PRELIQ | Liquid precipitation (rain-on-snow melt) | mm |
| FF | Wind speed | m/s |
| SSI | Visible radiation | J/cm² |
| DLI | Atmospheric radiation | J/cm² |
| HU | Relative humidity | % |
| Q | Specific humidity | g/kg |
| ETP | Potential evapotranspiration | mm |
| HTEURNEIGE | Snow depth at day J | m |
| RESR_NEIGE | Snow water equivalent at day J | mm |
| SNOW_FRAC | Snow cover fraction | % |
| ECOULEMENT | Snowmelt runoff at base of snowpack | mm |
| SWI | Soil wetness index | % |

## Target

Your model must predict `HTEURNEIGE_J7`: the **snow depth in meters at day J+7**
for each grid point.

## Evaluation

Submissions are evaluated using **RMSE** (Root Mean Squared Error, in meters) as
the primary metric. Lower is better. A secondary metric is also reported:
- **MAE** (Mean Absolute Error, in meters)

See the **Timeline** page for the competition phases.

# Reminder : The data is available in Get Started / Files / input_data