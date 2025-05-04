FROM python:3.12.3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY model_service/ model_service/
ENV PYTHONPATH=/app
CMD ["python", "model_service/service.py"]
