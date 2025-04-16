from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib
import os
import requests
from typing import Union

app = FastAPI()

# 📦 URL du modèle Hugging Face
MODEL_URL = "https://huggingface.co/FMendes13/getaround-pricing-model/resolve/main/rf_model_top11.pkl"
MODEL_PATH = "/tmp/rf_model_top11.pkl"

# ⬇️ Télécharger le modèle s’il n’existe pas localement
if not os.path.exists(MODEL_PATH):
    try:
        print("⏬ Téléchargement du modèle...")
        response = requests.get(MODEL_URL)
        response.raise_for_status()
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print("✅ Modèle téléchargé.")
    except Exception as e:
        print("❌ Échec du téléchargement du modèle :", str(e))

# 📥 Chargement du modèle
try:
    model = joblib.load(MODEL_PATH)
    print("✅ Modèle chargé avec succès.")
except Exception as e:
    print("❌ Erreur lors du chargement du modèle :", str(e))
    model = None

# 🔢 Types mixtes pour les features
class InputData(BaseModel):
    input: list[list[Union[float, int, str]]]

# 🏠 Page d’accueil
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <head><title>Getaround API</title></head>
      <body style="font-family: Arial, sans-serif; margin: 2rem;">
        <h1>🚗 Getaround Pricing API</h1>
        <p>✅ L'API est en ligne.</p>
        <p>Utilisez l'endpoint <code>/predict</code> en POST pour faire des prédictions.</p>
        <p><a href="/docs">📄 Voir la documentation</a></p>
      </body>
    </html>
    """

# 🔮 Endpoint de prédiction
@app.post("/predict")
def predict(data: InputData):
    try:
        if model is None:
            return {"error": "Model not loaded"}

        input_df = pd.DataFrame(data.input, columns=[
            "mileage", "engine_power", "fuel", "paint_color", "car_type",
            "private_parking_available", "has_gps", "has_air_conditioning",
            "automatic_car", "has_getaround_connect", "has_speed_regulator"
        ])

        prediction = model.predict(input_df).tolist()
        return {"prediction": prediction}

    except Exception as e:
        return {"error": str(e)}

# 📘 Doc HTML custom
@app.get("/docs", response_class=HTMLResponse)
def custom_docs():
    try:
        with open("docs.html", "r") as f:
            return HTMLResponse(content=f.read())
    except:
        return HTMLResponse(content="<h1>Documentation not found</h1>", status_code=404)
