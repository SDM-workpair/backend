FROM teamatch_backend:latest
WORKDIR /backend
CMD ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8001", "microservices.matching.main:app", "--reload"]