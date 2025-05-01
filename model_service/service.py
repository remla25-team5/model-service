from flask import Flask, request, jsonify
from model_service.model_utils import load_model
import os
# from lib_ml.preprocessing import preprocess_text

app = Flask(__name__)

# Load the model when the application starts
model = load_model()

# Get host and port from environment variables or use defaults
HOST = os.environ.get("MODEL_SERVICE_HOST", "0.0.0.0")
PORT = int(os.environ.get("MODEL_SERVICE_PORT", 5000))

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

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)