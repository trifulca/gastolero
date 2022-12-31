# Makefile

SHELL := /bin/bash

.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build-virtualenv: ## Build the virtualenv
	rm -rf .virtualenv
	python -m venv .virtualenv
	source .virtualenv/bin/activate && pip install -r requirements/local.txt

docker-build-dev: ## Build the Docker development image
	docker build -t gastolero-dev -f Dockerfile.dev .

docker-shell: ## Launch Docker shell
	docker run -it --name gastolero --rm \
		--volume $(shell pwd):/usr/app \
		--user $(shell id -u):$(shell id -g) \
		--net=host gastolero-dev:latest

docker-runserver: ## Lauch Django's runserver
	docker run -it --name gastolero --rm \
		--volume $(shell pwd):/usr/app \
		--user $(shell id -u):$(shell id -g) \
		--net=host gastolero-dev:latest bash -c "cd gastolero && ./manage.py runserver"
