from flask import Flask, request, render_template, jsonify
import pickle
import numpy as np

# Load the RandomForest model and encoders
with open('random_forest_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('label_encoders.pkl', 'rb') as encoders_file:
    label_encoders = pickle.load(encoders_file)

app = Flask(__name__)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from form
        vehicle_age = int(request.form['vehicle_age'])
        km_driven = int(request.form['km_driven'])
        seller_type = request.form['seller_type']
        fuel_type = request.form['fuel_type']
        transmission_type = request.form['transmission_type']
        mileage = float(request.form['mileage'])
        engine = int(request.form['engine'])
        max_power = float(request.form['max_power'])
        seats = int(request.form['seats'])

        # Encode categorical variables
        features = [
            vehicle_age,
            km_driven,
            label_encoders['seller_type'].transform([seller_type])[0],
            label_encoders['fuel_type'].transform([fuel_type])[0],
            label_encoders['transmission_type'].transform([transmission_type])[0],
            mileage,
            engine,
            max_power,
            seats
        ]
        
        # Predict the selling price
        prediction = model.predict([features])[0]
        output = round(prediction, 2)

        # Render the template with the prediction and form data
        return render_template('index.html', 
                               prediction_text=f'Estimated Selling Price: ₹{output}',
                               form_data={
                                   'vehicle_age': vehicle_age,
                                   'km_driven': km_driven,
                                   'seller_type': seller_type,
                                   'fuel_type': fuel_type,
                                   'transmission_type': transmission_type,
                                   'mileage': mileage,
                                   'engine': engine,
                                   'max_power': max_power,
                                   'seats': seats
                               })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
