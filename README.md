# Model-Service

This repository represents a wrapper service for the released ML model. It has a REST API to
expose the model to other components.

## Environment Variables

The service can be configured using the following environment variables:

- `MODEL_URL`: Required. URL from which to download the ML model.
- `CV_URL`: Required. URL from which to download the CountVectorizer.
- `MODEL_VERSION`: Optional. Version identifier for the model. Defaults to "0.0.1".
- `MODEL_CACHE_DIR`: Optional. Directory where models will be cached. Defaults to local "model-cache" directory.
- `CV_CACHE_DIR`: Optional. Directory where CountVectorizers will be cached. Defaults to local "cv-cache" directory.
- `MODEL_SERVICE_HOST`: Optional. Host address for the service. Defaults to "0.0.0.0".
- `MODEL_SERVICE_PORT_NUMBER`: Optional. Port for the service. Defaults to 5000.

## API Endpoints

The service exposes the following endpoints:

- `POST /predict`: Predicts sentiment from text. Requires a JSON body with a "text" field.
- `GET /version`: Returns the current version of the lib-ml model.

## Model Caching Strategy

The service implements a caching strategy to avoid downloading the model and CountVectorizer on every container start:

1. Models are cached in the directory specified by `MODEL_CACHE_DIR` environment variable
2. CountVectorizers are cached in the directory specified by `CV_CACHE_DIR` environment variable
3. Different model versions are stored with distinct filenames based on the `MODEL_VERSION` environment variable
4. On startup, the service checks if the requested model and CountVectorizer already exist in the cache
5. The files are only downloaded if they don't exist in the cache

For production deployments, it's recommended to mount persistent volumes to the `MODEL_CACHE_DIR` and `CV_CACHE_DIR` paths to preserve the cache between container restarts or when scaling horizontally.

## Example Docker Run with Volume Mount

```bash
docker run -p 5000:5000 \
  --env-file=.env \
  -v /host/path/to/model-cache:/app/model-cache \
  -v /host/path/to/cv-cache:/app/cv-cache \
  ghcr.io/remla25-team5/model-service:latest
```

## Example .env File

The `.env` file should contain the following environment variables for the service to function properly:

```
MODEL_SERVICE_HOST=0.0.0.0
MODEL_SERVICE_PORT_NUMBER=5000
MODEL_CACHE_DIR=./model-cache
CV_CACHE_DIR=./cv-cache
MODEL_VERSION=0.0.1
MODEL_URL=https://github.com/remla25-team5/model-training/releases/download/{MODEL_VERSION}/c2_Classifier_Sentiment_Model.joblib
CV_URL=https://github.com/remla25-team5/model-training/releases/download/{MODEL_VERSION}/c1_BoW_Sentiment_Model.pkl
```

Note that `{MODEL_VERSION}` in the URLs will be automatically replaced with the value of `MODEL_VERSION`. You can modify these variables according to your specific deployment requirements.

## Running Locally

To run the service on your local machine for development or testing:

1.  **Prerequisites:**
    * Docker

2.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder-name>
    ```

3.  **Create your `.env` file:**
    Copy the example `.env` content from above (or create your own) in the project root directory.

6.  **Run the service:**
    Use the docker file to run the service:
    ```bash
    docker build -t model-service .

    docker run -p 5000:5000 --env-file=.env model-service
    ```

    The service should now be running and accessible, typically at `http://localhost:5000` (or the host/port configured in your `.env` file and used by the application).