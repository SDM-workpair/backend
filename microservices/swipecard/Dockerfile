FROM teamatch_backend:latest
WORKDIR /backend
CMD ["python", "-m", "uvicorn", "--host", "0.0.0.0", "--port", "8002", "microservices.swipecard.swipe:app", "--reload"]