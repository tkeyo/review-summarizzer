IMAGE_NAME=review-summarizzer
PORT=8080

.PHONY: help build run

help:
	@echo "Makefile for Dockerized FastAPI app"
	@echo "Available targets:"
	@echo "  build   Build the Docker image."
	@echo "  run     Run the Docker container (binds to port $(PORT))."

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --rm -it -p $(PORT):8080 --env-file .env $(IMAGE_NAME) && docker rmi $(IMAGE_NAME) 