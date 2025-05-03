import os
import requests
import joblib
from pathlib import Path

# Get model cache directory from environment variable or use default
MODEL_CACHE_DIR = os.environ.get("MODEL_CACHE_DIR", "/app/model-cache")
MODEL_VERSION = os.environ.get("MODEL_VERSION", "latest")


def get_model_path():
    """
    Get the path to the model file based on the MODEL_VERSION.
    Creates the cache directory if it doesn't exist.
    """
    # Create cache directory if it doesn't exist
    Path(MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)
    
    # Use the model version in the filename
    return os.path.join(MODEL_CACHE_DIR, f"model_{MODEL_VERSION}.pkl")


def download_model():
    """
    Download the model from a given URL and save it to the specified path.
    Uses MODEL_VERSION to manage different versions of the model.
    """
    url = os.environ.get("MODEL_URL")

    if not url:
        raise ValueError("MODEL_URL environment variable is not set.")
    
    model_path = get_model_path()
    
    # Check if the model already exists in cache
    if os.path.exists(model_path):
        print(f"Model version {MODEL_VERSION} already exists at {model_path}. Using cached version.")
        return model_path
    
    # Download the model
    print(f"Downloading model version {MODEL_VERSION} from {url}...")

    # Check if the URL is valid
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save to the cache location
        with open(model_path, "wb") as f:
            f.write(response.content)
        print(f"Model downloaded and saved to {model_path}")
        return model_path
    else:
        print(f"Failed to download model. Status code: {response.status_code}")
        raise RuntimeError(f"Failed to download model from {url}")


def load_model():
    """
    Load the model from the specified path.
    Downloads the model if it doesn't exist in the cache.
    """
    # Download the model if needed and get the path
    model_path = download_model()

    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)

    print(f"Model version {MODEL_VERSION} loaded successfully.")
    return model