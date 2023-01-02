SHELL := /bin/bash
include config.env

DOCKER_RUN_BASE := docker run -it --rm
DOCKER_RUN_BASE += --volume $(shell pwd):/usr/app
DOCKER_RUN_BASE += --user $(shell id -u):$(shell id -g)
DOCKER_RUN_BASE += --net=host $(APP_NAME)-dev:latest

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

docker-build-dev: ## Build the Docker development image
	docker build -t $(APP_NAME)-dev -f Dockerfile.dev .

docker-shell: ## Launch Docker shell
	$(DOCKER_RUN_BASE)

docker-runserver: ## Lauch Django's runserver
	$(DOCKER_RUN_BASE) bash -c "cd gastolero && ./manage.py runserver"

docker-makemigrations: ## Update Django's migrations
	$(DOCKER_RUN_BASE) bash -c "cd gastolero && ./manage.py makemigrations"
