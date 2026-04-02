from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


def train_model(X, y, feature_names):
    """
    Train Random Forest model and save it.

    Args:
        X: feature matrix
        y: target variable
        feature_names: list of feature column names
    """

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Create model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    # Train
    model.fit(X_train, y_train)

    # Save model bundle
    bundle = {
        "model": model,
        "feature_names": feature_names
    }

    model_path = Path("models/rain_model.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(bundle, model_path)

    print("✅ Model trained and saved at:", model_path)

    return model
