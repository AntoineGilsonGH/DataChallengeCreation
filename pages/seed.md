# Seed

Your `submission.py` must define a `get_model()` function returning an object
with `fit()` and `predict()` methods compatible with the scikit-learn API.

Below is the baseline submission provided as a starting point.
You are free to replace the `RandomForestRegressor` with any model of your choice.

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
 
FEATURES = [
    "LAMBX", "LAMBY",
    "T", "TINF_H", "TSUP_H",
    "PRENEI", "PRELIQ",
    "FF", "SSI", "DLI", "HU", "Q", "ETP",
    "HTEURNEIGE", "RESR_NEIGE", "SNOW_FRAC", "ECOULEMENT",
    "SWI",
]

def get_model():
    return SnowDepthModel()

class SnowDepthModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )

    def fit(self, X, y):
        """
        Train the model.
        X : pd.DataFrame — features at day J (see feature list above)
        y : pd.Series   — HTEURNEIGE_J7, snow depth in meters at day J+7
        """
        self.model.fit(X[FEATURES], y)
        return self

    def predict(self, X):
        """
        Generate predictions.
        X : pd.DataFrame — same columns as training data
        Returns: np.array of predicted snow depth in meters (clipped to >= 0)
        """
        preds = self.model.predict(X[FEATURES])
        return preds.clip(min=0)
```
