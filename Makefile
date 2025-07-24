# Django News Portal Makefile
# Simplifies common development and deployment tasks

.PHONY: help install dev-setup migrate test docker-build docker-run docker-stop clean docs

# Default target
help:
	@echo "Django News Portal - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make install      - Install Python dependencies"
	@echo "  make dev-setup    - Set up development environment"
	@echo "  make migrate      - Run database migrations"
	@echo "  make test         - Run tests"
	@echo "  make runserver    - Start development server"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make docker-stop  - Stop Docker container"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs         - Generate Sphinx documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Clean up temporary files"

# Install dependencies
install:
	pip install -r requirements.txt

# Development environment setup
dev-setup: install
	python manage.py migrate
	python manage.py collectstatic --noinput

# Run database migrations
migrate:
	python manage.py migrate

# Run tests
test:
	python manage.py test
	# Alternative: pytest

# Start development server
runserver:
	python manage.py runserver 0.0.0.0:8000

# Docker commands
docker-build:
	docker build -t django-news-portal .

docker-run:
	docker run -p 8000:8000 django-news-portal

docker-stop:
	docker stop $$(docker ps -q --filter ancestor=django-news-portal)

# Generate documentation
docs:
	cd docs && make html

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	rm -rf .coverage htmlcov/
