import os
import requests
import joblib

MODEL_PATH = "model.pkl"


def download_model():
    """
    Download the model from a given URL and save it to the specified path.
    """
    url = os.environ.get("MODEL_URL")

    if not url:
        raise ValueError("MODEL_URL environment variable is not set.")
    
    # Check if the model already exists
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at {MODEL_PATH}. Skipping download.")
        return
    
    # Download the model
    print(f"Downloading model from {url}...")

    # Check if the URL is valid
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(MODEL_PATH, "wb") as f:
            f.write(response.content)
        print(f"Model downloaded and saved to {MODEL_PATH}")
    else:
        print(f"Failed to download model. Status code: {response.status_code}")


def load_model():
    """
    Load the model from the specified path.
    """
    # Download the model
    download_model()

    print(f"Loading model from {MODEL_PATH}...")
    model = joblib.load(MODEL_PATH)

    print("Model loaded successfully.")
    return model