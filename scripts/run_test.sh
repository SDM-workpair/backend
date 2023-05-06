#!/bin/sh
ENTRYPOINT="python -m pytest --cov=app --html=test/report/report.html -W ignore::DeprecationWarning -s --capture=fd --log-cli-level=INFO --profile"
docker-compose up --build -d
docker-compose exec backend $ENTRYPOINT
# docker-compose exec backend poetry run scalene microservices/matching/matching_event.py  --use-virtual-time --cpu-percent-threshold 0.1 --reduced-profile