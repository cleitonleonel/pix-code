.PHONY: install lint format test check precommit

# Instala dependências
install:
	poetry install

# Lint com Ruff
lint:
	poetry run ruff check .

# Format com Ruff
format:
	poetry run ruff format .

# Testes com pytest
test:
	poetry run pytest

# Rodar pre-commit em todos arquivos
precommit:
	poetry run pre-commit run --all-files

# Checa tudo: lint, format, test
check: lint format test
