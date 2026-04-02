from pathlib import Path

import pandas as pd
from sklearn.preprocessing import LabelEncoder


def load_and_clean_data(file_path: str | Path) -> tuple[pd.DataFrame, LabelEncoder]:
    """
    Load the weather dataset, clean missing values, and encode the target column.

    Args:
        file_path: Path to the CSV dataset.

    Returns:
        A tuple containing:
        - cleaned pandas DataFrame
        - fitted LabelEncoder for RainTomorrow
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {file_path}")

    df = pd.read_csv(file_path)

    # Remove rows where the target is missing
    df = df.dropna(subset=["RainTomorrow"]).copy()

    # Select columns needed for training
    required_columns = [
        "MinTemp",
        "MaxTemp",
        "Humidity9am",
        "Humidity3pm",
        "Pressure9am",
        "Pressure3pm",
        "WindSpeed9am",
        "WindSpeed3pm",
        "RainTomorrow",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in dataset: {missing_columns}")

    df = df[required_columns].copy()

    # Fill missing feature values
    feature_columns = [col for col in required_columns if col != "RainTomorrow"]
    df[feature_columns] = df[feature_columns].ffill().bfill()

    # Drop any remaining nulls just in case
    df = df.dropna().copy()

    # Encode target column: No -> 0, Yes -> 1
    label_encoder = LabelEncoder()
    df["RainTomorrow"] = label_encoder.fit_transform(df["RainTomorrow"])

    return df, label_encoder
