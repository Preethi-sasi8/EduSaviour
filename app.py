from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

risk_model = joblib.load("risk_model.pkl")
scheme_model = joblib.load("scheme_model.pkl")
model_columns = joblib.load("model_columns.pkl")

@app.route("/predict", methods=["POST"])
def predict():


   data = request.json

   df = pd.DataFrame([data])

# convert categorical variables
   df = pd.get_dummies(df)

# match training columns
   df = df.reindex(columns=model_columns, fill_value=0)

# predictions
   risk = risk_model.predict(df)[0]
   scheme = scheme_model.predict(df)[0]

# top factors using feature importance
   importance = risk_model.feature_importances_

   feature_importance = dict(zip(model_columns, importance))

   top3 = sorted(feature_importance.items(),
              key=lambda x: x[1],
              reverse=True)[:3]

   top_factors = [i[0] for i in top3]

   return jsonify({
    "Risk_Level": risk,
    "Recommended_Scheme": scheme,
    "Top_Influencing_Factors": top_factors
   })


if __name__ == "__main__":
   app.run(debug=True)

