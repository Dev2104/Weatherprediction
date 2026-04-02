from pathlib import Path
import joblib
import pandas as pd


def load_model(model_path="models/rain_model.pkl"):
    """
    Load trained model bundle
    """
    model_path = Path(model_path)

    if not model_path.exists():
        raise FileNotFoundError("Model not found. Train the model first.")

    bundle = joblib.load(model_path)
    return bundle


def predict_rain(input_data: dict):
    """
    Predict rain based on input features

    Args:
        input_data: dictionary with feature values

    Returns:
        prediction (0/1)
    """

    bundle = load_model()

    model = bundle["model"]
    feature_names = bundle["feature_names"]

    # Convert input to DataFrame
    df = pd.DataFrame([input_data])

    # Ensure correct feature order
    df = df[feature_names]

    prediction = model.predict(df)[0]

    return int(prediction)

