FROM python:3.12.3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY model_service/ model_service/
ENV PYTHONPATH=/app
ENV DOCKER_CONTAINER=true
ENV MODEL_VERSION=0.0.1
ENV MODEL_CACHE_DIR=/app/model-cache
ENV CV_CACHE_DIR=/app/cv-cache
ENV MODEL_SERVICE_HOST=0.0.0.0
ENV MODEL_SERVICE_PORT=5000
# Note: MODEL_URL and CV_URL must be provided at runtime
CMD ["python", "model_service/service.py"]
