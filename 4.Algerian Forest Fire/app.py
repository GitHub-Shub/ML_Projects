from flask import Flask, render_template, request
import numpy as np
import pickle

app = Flask(__name__)

# Load the trained model and scaler
with open('linreg.pkl', 'rb') as model_file:
    linreg = pickle.load(model_file)

with open('scalar.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Fire Risk Assessment Function
def assess_fire_risk(fwi_value):
    if fwi_value < 6:
        return "Minimal Risk"
    elif 6 <= fwi_value < 21:
        return "Low Risk"
    elif 21 <= fwi_value < 41:
        return "Moderate Risk"
    elif 41 <= fwi_value < 76:
        return "High Risk"
    elif 76 <= fwi_value < 100:
        return "Very High Risk"
    else:
        return "Extreme Risk"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve input values from the form
    temperature = float(request.form['Temperature'])
    rh = float(request.form['RH'])
    ws = float(request.form['Ws'])
    rain = float(request.form['Rain'])
    ffmc = float(request.form['FFMC'])
    dmc = float(request.form['DMC'])
    dc = float(request.form['DC'])
    isi = float(request.form['ISI'])
    bui = float(request.form['BUI'])
    
    # Prepare the input data for the model
    input_data = np.array([[temperature, rh, ws, rain, ffmc, dmc, dc, isi, bui]])
    input_data_scaled = scaler.transform(input_data)

    # Predict FWI value
    fwi_pred = linreg.predict(input_data_scaled)[0]
    
    # Assess fire risk based on FWI value
    fire_risk = assess_fire_risk(fwi_pred)

    # Prepare prediction text to display
    prediction_text = f"Predicted Fire Weather Index (FWI): {fwi_pred:.2f}, Fire Risk Level: {fire_risk}"

    # Render the template with input values and prediction
    return render_template('index.html', 
                           prediction_text=prediction_text,
                           temperature=temperature,
                           rh=rh,
                           ws=ws,
                           rain=rain,
                           ffmc=ffmc,
                           dmc=dmc,
                           dc=dc,
                           isi=isi,
                           bui=bui)
if __name__ == '__main__':
    app.run(debug=True)
