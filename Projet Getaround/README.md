# 🚗 Getaround - Machine Learning API

Ce projet propose une API en ligne permettant de prédire un prix de location journalier optimal pour des véhicules, basée sur les données internes de Getaround.

---

## 📦 Fonctionnalités

- Modèle RandomForest entraîné sur 11 variables sélectionnées.
- API en ligne via FastAPI, déployée sur Hugging Face Spaces.
- Endpoint `/predict` disponible avec réponse JSON.
- Documentation personnalisée sur `/docs`.

---

## 🌐 API publique en ligne

🔗 **API Hugging Face** : [https://FMendes13-getaround-api.hf.space](https://FMendes13-getaround-api.hf.space)  
🔗 **Documentation interactive Swagger** : [https://FMendes13-getaround-api.hf.space/docs](https://FMendes13-getaround-api.hf.space/docs)

---

## ⚙️ Exemple de requête POST `/predict`

### 🔢 Exemple d'input JSON

```json
{
  "input": [
    [170000, 45000, "diesel", "black", "convertible", 0, 1, 1, 0, 1, 0]
  ]
}
