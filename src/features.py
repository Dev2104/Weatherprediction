def select_features(df):
    """
    Select relevant features for rain prediction.

    Args:
        df: Cleaned pandas DataFrame

    Returns:
        X: feature matrix
        y: target variable
        features: list of feature names
    """

    features = [
        "MinTemp",
        "MaxTemp",
        "Humidity9am",
        "Humidity3pm",
        "Pressure9am",
        "Pressure3pm",
        "WindSpeed9am",
        "WindSpeed3pm"
    ]

    X = df[features]
    y = df["RainTomorrow"]

    return X, y, features
