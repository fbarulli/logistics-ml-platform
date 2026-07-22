.PHONY: up down build load train train-logs

CLUSTER_NAME := logistics-ml
TRAINING_IMAGE := training:local

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

load:
	docker compose run --rm etl

train:
	docker build -t $(TRAINING_IMAGE) -f docker/training/Dockerfile .
	kind load docker-image $(TRAINING_IMAGE) --name $(CLUSTER_NAME)
	kubectl delete job training -n database --ignore-not-found
	kubectl apply -f k8s/training-job.yaml
	kubectl wait --for=condition=ready pod -l job-name=training -n database --timeout=120s
	kubectl logs -f -n database job/training

train-logs:
	kubectl logs -f -n database job/training
