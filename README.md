# FareCast -- Uber Fare Prediction

Streamlit app that predicts NYC ride fares from pickup/drop-off, passenger count, ride type, and pickup time.

## Structure

```
uber-fare-app/
├── requirements.txt
├── .streamlit/config.toml      # theme + server settings for deploy
├── .python-version             # Python 3.11 (Streamlit Cloud)
├── Model/artifacts/            # drop trained *.joblib files here
└── app/
    ├── main.py                 # entry point
    ├── bootstrap.py            # creates dirs + demo model on first boot
    ├── config.py
    ├── core/
    ├── db/
    └── ui/
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

Open `http://localhost:8501`.

If no trained model exists yet, the app auto-creates a lightweight demo artifact so predictions still work locally.

## Model artifacts

Drop trained files into `Model/artifacts/`. Each `.joblib` must unpickle to:

```python
{
    "model_name": str,
    "model": ...,                   # has .predict()
    "scaler": StandardScaler,
    "feature_columns": list[str],
    "target_column": "fare_amount",
    "metrics": {"train": {...}, "test": {"mae": ..., "rmse": ..., "r2": ...}},
}
```

Default artifact loaded by the app: `random_forest_regression.joblib`

To generate a demo artifact manually:

```bash
python scripts/create_demo_artifact.py
```

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (public repo required for free tier).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** and fill in:
   - **Repository**: `your-username/uber-fare-app`
   - **Branch**: `main`
   - **Main file path**: `app/main.py`
4. Click **Deploy**.

Streamlit Cloud reads `requirements.txt` from the repo root and uses Python 3.11 (from `.python-version`).

### Deploy checklist

| Item | Location |
|------|----------|
| Dependencies | `requirements.txt` |
| Entry point | `app/main.py` |
| Theme / server config | `.streamlit/config.toml` |
| Python version | `.python-version` -> `3.11` |
| Model files | `Model/artifacts/*.joblib` (commit real models, or let bootstrap create a demo) |
| Secrets | not required for this app |

### Notes for production server

- **SQLite history** (`app/db/predictions.db`) is ephemeral on Streamlit Cloud -- it resets when the app reboots or redeploys. Trip history works during a session but is not permanent storage.
- **Commit real model artifacts** before deploy if you want production-grade predictions. The auto-generated demo model is only a fallback.
- **Do not commit** `.streamlit/secrets.toml` or local `*.db` files (already in `.gitignore`).

## GitHub push (first time)

```bash
cd uber-fare-app
git init
git add .
git commit -m "Initial commit: FareCast Streamlit app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/uber-fare-app.git
git push -u origin main
```

Then connect the repo on Streamlit Cloud as described above.

## Tabs

- **Plan trip** -- map + ride selection + fare estimate
- **Trip history** -- recent predictions from SQLite
- **Models** -- MAE / RMSE / R2 comparison across artifacts
