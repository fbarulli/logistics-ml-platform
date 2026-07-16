.PHONY: up down build load train

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

load:
	docker compose run --rm etl

train:
	docker compose run --rm training
