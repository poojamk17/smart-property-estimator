
import json
from pathlib import Path

# Load the exported Random Forest
MODEL_PATH = Path(__file__).parent / "house_price_forest.json"

with open(MODEL_PATH, "r", encoding="utf-8") as f:
    forest = json.load(f)


def predict_tree(tree, features):
    """Predict using one decision tree."""

    node = 0

    while tree["children_left"][node] != -1:
        feature_index = tree["feature"][node]
        threshold = tree["threshold"][node]

        if features[feature_index] <= threshold:
            node = tree["children_left"][node]
        else:
            node = tree["children_right"][node]

    return tree["value"][node]


def predict(features):
    """Average predictions from all trees in the forest."""

    if len(features) != forest["n_features"]:
        raise ValueError(
            f"Expected {forest['n_features']} features, "
            f"received {len(features)}."
        )

    predictions = [
        predict_tree(tree, features)
        for tree in forest["trees"]
    ]

    return sum(predictions) / len(predictions)