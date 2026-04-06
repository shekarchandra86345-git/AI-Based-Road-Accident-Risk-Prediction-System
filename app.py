from flask import Flask, render_template, request, jsonify, session, redirect
import pickle
import numpy as np
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = 'accident_guard_secret_key_2026'

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

def get_risk_reasons(data, prediction):
    reasons = []
    if int(data.get('speed', 0)) > 80:
        reasons.append(f"High speed ({data.get('speed')} km/h) increases accident risk significantly.")
    elif int(data.get('speed', 0)) > 60:
        reasons.append(f"Moderate speed ({data.get('speed')} km/h) – stay alert.")

    weather_map = {"0": "Clear", "1": "Rainy", "2": "Foggy", "3": "Snowy"}
    weather = str(data.get('weather', '0'))
    if weather in ["1", "2", "3"]:
        reasons.append(f"Weather is {weather_map.get(weather, 'Poor')} – reduces road visibility and grip.")

    surface_map = {"0": "Dry", "1": "Wet", "2": "Icy/Slippery"}
    surface = str(data.get('surface_condition', '0'))
    if surface in ["1", "2"]:
        reasons.append(f"Road surface is {surface_map.get(surface, 'Hazardous')} – slipping risk is elevated.")

    if int(data.get('light_condition', 0)) == 1:
        reasons.append("Night-time driving significantly increases accident probability.")

    road_map = {"0": "Local Street", "1": "Main Road", "2": "Highway"}
    road = str(data.get('road_type', '0'))
    if road == "2":
        reasons.append("Highway roads carry higher risk at increased speeds.")

    traffic_map = {"0": "Low", "1": "Moderate", "2": "High"}
    traffic = str(data.get('traffic_density', '0'))
    if traffic == "2":
        reasons.append("High traffic density raises the chance of collisions.")

    age = int(data.get('driver_age', 30))
    exp = int(data.get('driver_experience', 5))
    if age < 25:
        reasons.append(f"Young driver (age {age}) – statistically higher accident risk.")
    if exp < 2:
        reasons.append("Inexperienced driver (less than 2 years) – higher probability of errors.")

    hour = int(data.get('hour_of_day', 12))
    if hour >= 22 or hour <= 5:
        reasons.append(f"Late night/early morning hours ({hour}:00) are high-risk time windows.")

    # Accident history (14th feature)
    acc = int(data.get('accident_count', 0))
    if acc >= 20:
        reasons.append(f"This location has a high accident history ({acc} past accidents) — a confirmed danger hotspot.")
    elif acc >= 5:
        reasons.append(f"This location has a moderate accident history ({acc} past accidents) — exercise extra caution.")
    elif acc > 0:
        reasons.append(f"This location has a low accident record ({acc} past accidents) — generally safe historically.")

    if not reasons:
        if prediction == 0:
            reasons.append("All conditions are within safe limits. Stay alert and enjoy your journey!")
        elif prediction == 1:
            reasons.append("Conditions are slightly elevated. Drive cautiously.")
        else:
            reasons.append("Multiple risk factors detected. Please take extra care or consider an alternative route.")

    return reasons

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        # Build named DataFrame so feature names match training exactly
        FEATURE_COLS = [
            'lat', 'lon', 'driver_age', 'driver_experience', 'vehicle_age',
            'vehicle_type', 'speed', 'weather', 'road_type', 'light_condition',
            'traffic_density', 'surface_condition', 'hour_of_day', 'accident_count'
        ]
        feature_values = [
            float(data.get('lat', 0)),
            float(data.get('lon', 0)),
            int(data.get('driver_age', 30)),
            int(data.get('driver_experience', 5)),
            int(data.get('vehicle_age', 5)),
            int(data.get('vehicle_type', 0)),
            int(data.get('speed', 40)),
            int(data.get('weather', 0)),
            int(data.get('road_type', 0)),
            int(data.get('light_condition', 0)),
            int(data.get('traffic_density', 0)),
            int(data.get('surface_condition', 0)),
            int(data.get('hour_of_day', 12)),
            int(data.get('accident_count', 0))
        ]
        df_input = pd.DataFrame([feature_values], columns=FEATURE_COLS)

        # Get probability scores
        prediction_proba = model.predict_proba(df_input)[0]
        prediction = int(np.argmax(prediction_proba))
        risk_score = float(max(prediction_proba) * 100)

        risk_messages = {
            2: {"status": "Risky", "message": "High alert! This route is dangerous. Please avoid or drive with extreme caution.", "color": "#ff4d4d"},
            1: {"status": "Less Risky", "message": "Caution: Potential hazards ahead. Drive carefully and maintain a safe speed.", "color": "#ffa333"},
            0: {"status": "Safe", "message": "Routine conditions detected. Have a safe journey!", "color": "#2ecc71"}
        }

        result = risk_messages.get(prediction, {"status": "Unknown", "message": "Data insufficient", "color": "#95a5a6"})
        reasons = get_risk_reasons(data, prediction)
        
        # Save to session for the result page and chatbot
        session['last_prediction'] = {
            "prediction": prediction,
            "risk_status": result["status"],
            "message": result["message"],
            "color": result["color"],
            "probability": round(risk_score, 2),
            "reasons": reasons,
            "data": {k: str(v) for k, v in data.items()}
        }

        return jsonify({
            "status": "success",
            "prediction": prediction,
            "risk_status": result["status"],
            "message": result["message"],
            "color": result["color"],
            "probability": round(risk_score, 2),
            "reasons": reasons
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/result")
def result_page():
    pred = session.get('last_prediction')
    if not pred:
        return redirect('/')

    prediction = pred['prediction']
    probability = pred['probability']

    # Needle: prediction 0→-80°, 1→0°, 2→+80° (centre-sweep over 180°)
    needle_angles = {0: -82, 1: 0, 2: 82}
    needle_angle = needle_angles.get(prediction, 0)

    # Colour / icon per level
    style_map = {
        0: {"color": "#22c55e", "badge_bg": "#f0fdf4", "reason_bg": "#f0fdf4",
            "reason_border": "#bbf7d0", "reason_icon": "✅", "risk_icon": "✅"},
        1: {"color": "#f59e0b", "badge_bg": "#fffbeb", "reason_bg": "#fffbeb",
            "reason_border": "#fde68a", "reason_icon": "⚠️", "risk_icon": "⚠️"},
        2: {"color": "#ef4444", "badge_bg": "#fff1f2", "reason_bg": "#fff1f2",
            "reason_border": "#fecaca", "reason_icon": "🚨", "risk_icon": "🚨"},
    }
    style = style_map.get(prediction, style_map[1])

    return render_template("result.html",
        risk_status=pred['risk_status'],
        message=pred['message'],
        reasons=pred.get('reasons', []),
        probability=probability,
        needle_angle=needle_angle,
        **style
    )

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.get_json().get("message", "").lower().strip()
        pred = session.get('last_prediction', {})
        risk_status = pred.get('risk_status', 'Unknown')
        reasons = pred.get('reasons', [])
        reasons_text = " ".join(reasons)

        # Rule-based contextual chatbot
        responses = []

        if any(w in user_msg for w in ["hello", "hi", "hey"]):
            responses.append(f"Hello! I'm AccidentGuard AI. I can help you understand your route risk. Your current status is <strong>{risk_status}</strong>.")

        elif any(w in user_msg for w in ["why", "reason", "cause", "factor"]):
            if reasons:
                responses.append(f"Here are the main risk factors I detected:<br><ul>" + "".join([f"<li>{r}</li>" for r in reasons]) + "</ul>")
            else:
                responses.append("I couldn't find specific risk factors. Try submitting your route parameters first.")

        elif any(w in user_msg for w in ["safe", "safe route", "is it safe"]):
            if risk_status == "Safe":
                responses.append("✅ Your current route appears <strong>Safe</strong>. All conditions are within acceptable limits. Drive at a steady speed and stay attentive.")
            elif risk_status == "Less Risky":
                responses.append("⚠️ Your route is <strong>Less Risky</strong> but not entirely safe. I recommend reducing speed slightly and increasing following distance.")
            else:
                responses.append("🚨 Your route is currently <strong>Risky</strong>. Consider delaying travel, taking an alternate route, or driving at much lower speed.")

        elif any(w in user_msg for w in ["advice", "suggestion", "recommend", "tips", "what should"]):
            if risk_status == "Risky":
                responses.append("🚨 <strong>High Risk Advice:</strong><br>1. Avoid this route if possible.<br>2. Slow down below 40 km/h.<br>3. Keep hazard lights on in poor visibility.<br>4. Maintain extra distance from vehicles ahead.")
            elif risk_status == "Less Risky":
                responses.append("⚠️ <strong>Caution Advice:</strong><br>1. Reduce speed by 20-30%.<br>2. Avoid overtaking on bends.<br>3. Stay on well-lit portions of the road.")
            else:
                responses.append("✅ <strong>Safe Route Tips:</strong><br>1. Maintain a steady, legal speed.<br>2. Stay hydrated and avoid distractions.<br>3. Check your mirrors regularly.")

        elif any(w in user_msg for w in ["weather", "rain", "fog", "condition"]):
            responses.append("In adverse weather conditions, always reduce speed by 30-40%, turn on headlights, and maintain a 3-second following distance. Pull over if visibility drops below 50 meters.")

        elif any(w in user_msg for w in ["night", "dark", "driving at night"]):
            responses.append("Night driving is 3x riskier than daytime. Use high beams on empty roads, avoid over-speeding, and take breaks every 2 hours to combat drowsiness.")

        elif any(w in user_msg for w in ["speed", "fast", "slow down"]):
            responses.append("Speed is the #1 cause of fatal accidents. Reducing speed by just 10 km/h can cut accident severity by up to 40%. Always abide by posted limits.")

        elif any(w in user_msg for w in ["risk", "score", "probability"]):
            prob = pred.get('probability', 'N/A')
            responses.append(f"Your current route risk score is <strong>{prob}%</strong> with a status of <strong>{risk_status}</strong>. {pred.get('message', '')}")

        elif any(w in user_msg for w in ["help", "what can you do", "commands"]):
            responses.append("I can help you with:<br>🔹 <em>'Why is it risky?'</em> – Explain risk factors.<br>🔹 <em>'Is it safe?'</em> – Route safety assessment.<br>🔹 <em>'Give advice'</em> – Driving tips for your situation.<br>🔹 <em>'What is my score?'</em> – Your risk probability.")

        else:
            responses.append(f"I'm here to help with road safety guidance. Your current risk level is <strong>{risk_status}</strong>. Ask me 'why is it risky?' or 'give me advice' for more details.")

        return jsonify({"response": responses[0] if responses else "I'm not sure how to answer that. Try asking about your risk status or for safety tips."})

    except Exception as e:
        return jsonify({"response": "Sorry, I encountered an error. Please try again."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
