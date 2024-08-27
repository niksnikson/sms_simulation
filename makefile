# Variables
SENDER_COUNT ?= 1
MEAN_TIME ?= 1.5
FAIL_RATE ?= 0.2

# Build Docker images
build:
	docker-compose build
	
# Run RabbitMQ and Redis
run-services:
	docker-compose up -d rabbitmq redis

# Run Senders, specifying the number of instances
run-senders:
	docker-compose up -d --scale sender=$(SENDER_COUNT) sender

# Run Sender with custom params
run-sender:
	docker-compose run -d \
		sender python sender.py $(MEAN_TIME) $(FAIL_RATE)

# Run Producer
run-producer:
	docker-compose up -d producer

# Run Monitor
run-monitor:
	docker-compose up monitor

# Stop all running containers
stop:
	docker-compose stop

# Down all containers, networks, and volumes
down:
	docker-compose down -v

# Run Tests
test:
	pytest

# Run Test Coverage
coverage:
	coverage run -m pytest
	coverage report -m

# Clean __pycache__, .pytest_cache, .coverage, and tests/__pycache__
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .pytest_cache .coverage
	rm -rf tests/__pycache__

.PHONY: run-services run-senders run-producer run-monitor stop down test coverage clean
