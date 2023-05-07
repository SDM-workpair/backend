docker-compose build
docker-compose up -d

docker-compose exec backend alembic revision --autogenerate -m "Recreate all table"
docker-compose exec backend alembic upgrade head
docker-compose down