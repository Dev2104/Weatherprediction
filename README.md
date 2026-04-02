# weather_ml_app

Production-ready folder structure for a Weather ML + Streamlit application.

## Structure
- `app/`: Streamlit multi-page frontend (UI only)
- `src/`: Modular backend (API client, preprocessing, features, training, prediction, insights)
- `data/raw/`: Kaggle dataset drops (ignored by git)
- `data/processed/`: Cleaned/feature-ready data (ignored by git)
- `models/`: Trained artifacts (ignored by git)
- `notebooks/`: Experiments and EDA

## Notes
- Add secrets to `.env` (never commit real keys).
- Streamlit config lives in `.streamlit/config.toml`.

