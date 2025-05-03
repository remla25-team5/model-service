from flask import Flask, request, jsonify
from model_utils import load_model
from flasgger import Swagger, swag_from
import os
# from lib_ml.preprocessing import preprocess_text
# from lib_ml import __version__ as lib_ml_version

app = Flask(__name__)
swagger = Swagger(app)

# Load the model when the application starts
# model = load_model()

# Get host and port from environment variables or use defaults
HOST = os.environ.get("MODEL_SERVICE_HOST", "0.0.0.0")
PORT = int(os.environ.get("MODEL_SERVICE_PORT", 5000))

@app.route('/predict', methods=['POST'])
@swag_from('docs/predict.yml')
def predict():
    """
    Endpoint to make predictions using the loaded model.
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    text = data['text']
    
    # TODO: Preprocess the text
    # processed_text = preprocess_text(text)
    
    # Make prediction
    sentiment = True if model.predict([text])[0] == 1 else False
    
    return jsonify({"text": text, 'sentiment': sentiment})


@app.route('/version', methods=['GET'])
@swag_from('docs/version.yml')
def version():
    """
    Endpoint to get the version of the model from lib_ml.
    """
    # For now, we will return a hardcoded version
    return jsonify({"version": "1.0.0"})

    # TODO: Uncomment the following lines when lib_ml is available
    # return jsonify({"version": lib_ml_version})
    

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)