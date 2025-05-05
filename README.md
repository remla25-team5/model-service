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
- `MODEL_SERVICE_PORT`: Optional. Port for the service. Defaults to 5000.

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
  -e MODEL_URL=https://github.com/remla25-team5/model-training/releases/download/0.0.1/c2_Classifier_Sentiment_Model.joblib \
  -e CV_URL=https://github.com/remla25-team5/model-training/releases/download/0.0.1/c1_BoW_Sentiment_Model.pkl \
  -e MODEL_VERSION=0.0.1 \
  -v /host/path/to/model-cache:/app/model-cache \
  -v /host/path/to/cv-cache:/app/cv-cache \
  ghcr.io/remla25-team5/model-service:latest
```