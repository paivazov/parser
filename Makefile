.DEFAULT_GOAL := start


YAML_FILES := -f ./docker-compose.yml
NAME := -p site_parser
DOCKER=docker compose $(YAML_FILES) $(NAME)

BLACK=black --skip-string-normalization --line-length 79 --target-version py310


.PHONY: visit_to_app start migrations parse

start: migrations parse

# starts parsing from first page
parse:
	$(DOCKER) up -d database
	$(DOCKER) run --rm application python ./entrypoint.py 1
	$(DOCKER) stop database

# applies alembic migrations to database
migrations:
	$(DOCKER) up -d database
	$(DOCKER) run --rm application /bin/bash ./entrypoint.sh
	$(DOCKER) stop database

# creates access inside docker container
visit_to_app:
	$(DOCKER) up -d database
	$(DOCKER) run --rm application /bin/bash
	$(DOCKER) stop database

# linters
.PHONY:  format typecheck format_check  check format

typecheck:
	python -m mypy --pretty --show-error-codes .

format_check:
	python -m isort . --only-sections --quiet --check-only --diff \
              --line-length 79
	$(BLACK) --fast --check .

check: typecheck format_check

format:
	python -m isort . --only-sections
	$(BLACK) .
