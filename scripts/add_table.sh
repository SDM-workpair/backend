docker-compose build
docker-compose run backend alembic revision --autogenerate -m "Adjust MR_Member Table"
docker-compose run backend alembic upgrade head