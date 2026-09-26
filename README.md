
# 🏡 Haven — Smart Property Price Estimator

An interactive machine learning web application that estimates
neighborhood-level median house values in California using a
Random Forest regression model.

Built with Python, Streamlit, Folium, and a lightweight
JSON-based prediction engine.

## Overview

Haven allows users to select a location on an interactive
California map, enter neighborhood characteristics, and
generate a model-based housing value estimate.

The project demonstrates a complete practical ML workflow:
data preparation, model training, evaluation, model export,
custom inference, and interactive application development.

## Features

- Interactive California map for selecting geographic coordinates
- Editable neighborhood and housing characteristics
- Random Forest regression model with 100 estimators
- JSON-based model inference without scikit-learn at runtime
- Responsive Streamlit interface
- Estimated values displayed in US dollars

## Model

The model was trained using the California Housing dataset
available through scikit-learn.

The dataset contains 20,640 observations and eight input features.

### Input features

| Feature | Description |
|---|---|
| MedInc | Median income in tens of thousands of dollars |
| HouseAge | Median house age in years |
| AveRooms | Average rooms per household |
| AveBedrms | Average bedrooms per household |
| Population | Neighborhood population |
| AveOccup | Average occupants per household |
| Latitude | Geographic latitude |
| Longitude | Geographic longitude |

### Target

`MedHouseVal` represents the median house value for a
California census block group, in units of $100,000.

The app multiplies the model output by 100,000 to display
the estimate in dollars.

### Evaluation

The Random Forest model was evaluated on a held-out test set.

| Metric | Result |
|---|---:|
| Mean Absolute Error (MAE) | 0.327543 |
| R² score | 0.805123 |

The MAE corresponds to approximately $32,754 in target units.

These are the results from the original model evaluation.
They are not a guarantee of accuracy for a particular property
or for locations outside the training distribution.

## Project structure

```text
smart-property-estimator/
├── app.py
├── predictor.py
├── house_price_forest.json
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── tests/
│   └── test_predictor.py
└── assets/
    └── app_screenshot.png
```

## Installation

Python 3.14.2 was used during local development.

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/smart-property-estimator.git
cd smart-property-estimator
```

Create and activate a virtual environment.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run locally

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually:

http://localhost:8501

## Model inference

The trained forest is exported to `house_price_forest.json`.

The custom `predictor.py` traverses each decision tree
using the exported split thresholds and leaf values, then
averages the tree predictions.

This avoids loading the original scikit-learn model at
runtime.

## Limitations

- Estimates represent census block-group median values,
  not individual property appraisals.
- The dataset reflects historical housing data and may not
  represent current market prices.
- Predictions depend on the quality and range of the
  supplied neighborhood features.
- Map coordinates alone do not determine the other
  neighborhood characteristics.
- The model should not be used as the sole basis for
  financial or real-estate decisions.

## Disclaimer

This project is for educational and demonstration purposes.
Predictions are estimates and are not financial advice,
professional appraisals, or guaranteed market values.

## Acknowledgments

- California Housing dataset distributed through scikit-learn
- Streamlit for the interactive web application framework
- Folium and OpenStreetMap for map visualization

## License

This project is licensed under the MIT License.
See the `LICENSE` file for details.