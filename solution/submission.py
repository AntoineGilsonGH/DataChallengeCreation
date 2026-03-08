import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Features available in X_train and X_test

FEATURES = [
    "LAMBX", "LAMBY",        # spatial position
    "T", "TINF_H", "TSUP_H", # temperature (mean, min, max)
    "PRENEI", "PRELIQ",       # solid and liquid precipitation
    "FF", "SSI", "DLI",       # wind, visible and atmospheric radiation
    "HU", "Q", "ETP",         # humidity and evapotranspiration
    "HTEURNEIGE", "RESR_NEIGE", "SNOW_FRAC", "ECOULEMENT",  # snow state at day J
    "SWI",                    # soil wetness index
]


# The submission here should simply be a function that returns a model
# compatible with scikit-learn API
def get_model():
    return SnowDepthModel()


class SnowDepthModel:
    """
    Baseline model: Random Forest Regressor.
    Predicts snow depth (HTEURNEIGE) at J+7 from meteorological features at J.

    You can replace this with any model that implements fit() and predict().
    """

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )

    def fit(self, X, y):
        self.model.fit(X[FEATURES], y)
        return self

    def predict(self, X):
        preds = self.model.predict(X[FEATURES])
        # Snow depth cannot be negative
        return preds.clip(min=0)