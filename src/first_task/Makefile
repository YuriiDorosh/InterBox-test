.PHONY: build up down logs run-cache run-no-cache

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

run-cache:
	docker-compose run --rm app python main.py

run-no-cache:
	docker-compose run --rm app python main.py --no-cache
