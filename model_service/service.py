from flask import Flask, request, jsonify
from model_service.model_utils import load_model
# from lib_ml.preprocessing import preprocess_text

app = Flask(__name__)

# Load the model when the application starts
model = load_model()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions using the loaded model.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    text = data['text']
    
    # Preprocess the text
    # processed_text = preprocess_text(text)
    
    # Make prediction
    prediction = model.predict([text])
    
    return jsonify({"text": text, 'prediction': prediction})