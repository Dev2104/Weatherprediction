from pathlib import Path
import sys

# Make project root importable when running this script directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.preprocess import load_and_clean_data
from src.features import select_features
from src.train import train_model


def main():
    data_path = PROJECT_ROOT / "data" / "raw" / "weatherAUS.csv"

    df, label_encoder = load_and_clean_data(data_path)
    X, y, feature_names = select_features(df)

    train_model(X, y, feature_names)

    print("✅ Training pipeline completed successfully.")
    print(f"📁 Dataset used: {data_path}")
    print("💾 Model saved to: models/rain_model.pkl")
    print(f"🏷️ Encoded classes: {list(label_encoder.classes_)}")


if __name__ == "__main__":
    main()