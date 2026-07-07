# AI-Based Road Accident Risk Prediction System

This project is a web-based Flask application that predicts the risk of a road accident based on various factors such as weather, road conditions, speed, traffic density, and driver experience. 

It uses a Machine Learning model loaded from a `.pkl` file to calculate the probability of a safe, less risky, or risky situation on the road. The application also provides interactive data visualization (a custom speedometer) and an integrated AI Chatbot for driving advice based on current route risk.

## Project Structure

```text
MINI_Project/
├── app.py                   # Main Flask application that serves the web routes and chatbot
├── model.pkl                # Pre-trained machine learning model pickle file
├── train_model.py           # Script to (re)train the ML model
├── generate_data.py         # Script to generate synthetic/mock accident dataset
├── accident_data_v2.csv     # Historical accident data used for pseudo-random geographic hotspots
├── requirements.txt         # Required Python packages for this project
├── static/                  # Static files (CSS, Javascript, Images)
└── templates/               # HTML UI templates (index.html, result.html)
```

## Features

1. **Risk Prediction Dashboard**: Input the trip's parameters like driver details, road type, weather, and light condition to retrieve a risk prediction score from the ML model.
2. **Speedometer UI**: Interactive data visualization giving visual feedback (Safe, Less Risky, Risky) using dynamic needle angles.
3. **Smart Chatbot**: An AI assistant (`AccidentGuard AI`) that explains the generated risk assessment, highlights the leading factors to the current risk score, and shares practical defensive driving advice.
4. **Historical Accident Hotspot Setup**: Uses a deterministic coordinate-based lookup to warn users of consistent accident records near specific GPS coordinates.

## Prerequisites

Make sure you have **Python** (ideally `3.8` to `3.11`) installed on your system.

## Steps to Run the Project

Follow these steps to quickly run the AI accident risk predictor locally on your machine:

1. **Open a Terminal / Command Prompt**
2. **Navigate to the Project Directory** (Update the path based on where you kept the folder):
   ```bash
   cd path\to\MINI_Project
   ```

3. **(Optional but Recommended) Create and activate a Virtual Environment**
   Creating a virtual environment ensures this project's dependencies don't conflict with other Python projects on your machine.
   ```bash
   python -m venv .venv
   ```
   - **On Windows:**
     ```cmd
     .venv\Scripts\activate
     ```
   - **On macOS / Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install the Dependencies**
   Install all the required Python packages mentioned in the `requirements.txt` file (this will automatically fetch Flask, pandas, numpy, scikit-learn, etc.).
   ```bash
   pip install -r requirements.txt
   ```

5. **Train the Model (Optional step)**
   The project already ships with a pre-trained `model.pkl` file, so this step is optional. If you update the configuration inside `generate_data.py` or modify the model tuning in `train_model.py`, you can regenerate and retrain your model by running:
   ```bash
   python train_model.py
   ```

6. **Run the Application**
   Launch the Flask server:
   ```bash
   python app.py
   ```
   *(By default, the script will run in `debug=True` mode on port `5000`)*

7. **Access the Website**
   Open your preferred web browser (Chrome, Edge, etc.) and go to the local address:
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

Enter your test parameters in the form and click **"Predict Risk"** to see your customized evaluation and safety advice!
