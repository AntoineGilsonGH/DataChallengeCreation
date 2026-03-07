import json
from pathlib import Path

import numpy as np
import pandas as pd

EVAL_SETS = ["test", "private_test"]


def compute_metrics(predictions, targets):
    """
    Compute RMSE and MAE for snow depth prediction.

    - RMSE : Root Mean Squared Error in meters — main metric, lower is better
    - MAE  : Mean Absolute Error in meters — secondary metric
    """
    y_pred = predictions.fillna(0).values.flatten()
    y_true = targets["HTEURNEIGE_J7"].values

    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    mae  = float(np.mean(np.abs(y_true - y_pred)))

    return {"rmse": rmse, "mae": mae}


def main(reference_dir, prediction_dir, output_dir):
    scores = {}
    for eval_set in EVAL_SETS:
        print(f"Scoring {eval_set}")
        predictions = pd.read_csv(
            prediction_dir / f"{eval_set}_predictions.csv"
        )
        targets = pd.read_csv(
            reference_dir / f"{eval_set}_labels.csv"
        )
        set_scores = compute_metrics(predictions, targets)
        # Prefix scores with eval_set name to separate public/private
        for metric, value in set_scores.items():
            scores[f"{eval_set}_{metric}"] = value

    # Add train and test times in the score
    json_durations = (prediction_dir / "metadata.json").read_text()
    durations = json.loads(json_durations)
    scores.update(**durations)

    print(scores)

    # Write output scores
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "scores.json").write_text(json.dumps(scores))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Scoring program for codabench"
    )
    parser.add_argument(
        "--reference-dir",
        type=str,
        default="/app/input/ref",
        help="",
    )
    parser.add_argument(
        "--prediction-dir",
        type=str,
        default="/app/input/res",
        help="",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="/app/output",
        help="",
    )
    args = parser.parse_args()
    main(
        Path(args.reference_dir),
        Path(args.prediction_dir),
        Path(args.output_dir),
    )