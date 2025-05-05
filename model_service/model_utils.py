import os
import requests
import joblib
from pathlib import Path

# Get model cache directory from environment variable or use default
# Use local directory paths when running locally
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_CACHE_DIR = os.environ.get("MODEL_CACHE_DIR", os.path.join(BASE_DIR, "model-cache"))
CV_CACHE_DIR = os.environ.get("CV_CACHE_DIR", os.path.join(BASE_DIR, "cv-cache"))
MODEL_VERSION = os.environ.get("MODEL_VERSION", "0.0.1")


def get_model_path():
    """
    Get the path to the model file based on the MODEL_VERSION.
    Creates the cache directory if it doesn't exist.
    """
    # Create cache directory if it doesn't exist
    Path(MODEL_CACHE_DIR).mkdir(parents=True, exist_ok=True)
    
    # Use the model version in the filename
    return os.path.join(MODEL_CACHE_DIR, f"model_{MODEL_VERSION}.joblib")


def get_cv_path():
    """
    Get the path to the CountVectorizer file based on the MODEL_VERSION.
    Creates the cache directory if it doesn't exist.
    """
    # Create cache directory if it doesn't exist
    Path(CV_CACHE_DIR).mkdir(parents=True, exist_ok=True)
    
    # Use the model version in the filename
    return os.path.join(CV_CACHE_DIR, f"cv_{MODEL_VERSION}.pkl")


def download_model():
    """
    Download the model from a given URL and save it to the specified path.
    Uses MODEL_VERSION to manage different versions of the model.
    """
    url = os.environ.get("MODEL_URL").format(MODEL_VERSION=MODEL_VERSION)

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


def download_cv():
    """
    Download the CountVectorizer from a given URL and save it to the specified path.
    Uses MODEL_VERSION to manage different versions of the CountVectorizer.
    """
    url = os.environ.get("CV_URL").format(MODEL_VERSION=MODEL_VERSION)

    if not url:
        raise ValueError("CV_URL environment variable is not set.")
    
    cv_path = get_cv_path()
    
    # Check if the CountVectorizer already exists in cache
    if os.path.exists(cv_path):
        print(f"CountVectorizer version {MODEL_VERSION} already exists at {cv_path}. Using cached version.")
        return cv_path
    
    # Download the CountVectorizer
    print(f"Downloading CountVectorizer version {MODEL_VERSION} from {url}...")

    # Check if the URL is valid
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save to the cache location
        with open(cv_path, "wb") as f:
            f.write(response.content)
        print(f"CountVectorizer downloaded and saved to {cv_path}")
        return cv_path
    else:
        print(f"Failed to download CountVectorizer. Status code: {response.status_code}")
        raise RuntimeError(f"Failed to download CountVectorizer from {url}")


def load_model():
    """
    Load the model and CountVectorizer from the specified paths.
    Downloads them if they don't exist in the cache.
    
    Returns:
        tuple: (cv, model) - The loaded CountVectorizer and model objects
    """
    # Download the model and CountVectorizer if needed and get the paths
    cv_path = download_cv()
    model_path = download_model()

    print(f"Loading CountVectorizer from {cv_path}...")
    cv = joblib.load(cv_path)
    print(f"CountVectorizer version {MODEL_VERSION} loaded successfully.")

    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    print(f"Model version {MODEL_VERSION} loaded successfully.")
    
    return cv, model