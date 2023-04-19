#!/bin/sh
ENTRYPOINT="python -m pytest --cov=app --html=test/report/report.html -W ignore::DeprecationWarning -s --capture=fd --log-cli-level=INFO"
docker-compose up --build -d
docker-compose exec backend $ENTRYPOINT