# Model-Service

This repository represents a wrapper service for the released ML model. It has a REST API to
expose the model to other components.

## Environment Variables

The service can be configured using the following environment variables:

- `MODEL_URL`: Required. URL from which to download the ML model.
- `MODEL_VERSION`: Optional. Version identifier for the model. Defaults to "latest".
- `MODEL_CACHE_DIR`: Optional. Directory where models will be cached. Defaults to "/app/model-cache".
- `MODEL_SERVICE_HOST`: Optional. Host address for the service. Defaults to "0.0.0.0".
- `MODEL_SERVICE_PORT`: Optional. Port for the service. Defaults to 5000.

## Model Caching Strategy

The service implements a caching strategy to avoid downloading the model on every container start:

1. Models are cached in the directory specified by `MODEL_CACHE_DIR` environment variable
2. Different model versions are stored with distinct filenames based on the `MODEL_VERSION` environment variable
3. On startup, the service checks if the requested model version already exists in the cache
4. The model is only downloaded if it doesn't exist in the cache

For production deployments, it's recommended to mount a persistent volume to the `MODEL_CACHE_DIR` path to preserve the cache between container restarts or when scaling horizontally.

## Example Docker Run with Volume Mount

```bash
docker run -p 5000:5000 \
  -e MODEL_URL=https://example.com/models/sentiment_v2.pkl \
  -e MODEL_VERSION=v2 \
  -v /host/path/to/model-cache:/app/model-cache \
  model-service
```