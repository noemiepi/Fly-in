# ----------------- #
#     Variables     #
# ----------------- #

PYTHON=uv run python

FLAKE8=uv run flake8
MYPY=uv run mypy

CHECK_UV=command -v uv
INSTALL_UV = curl -LsSf https://astral.sh/uv/install.sh | sh

MYPY_FLAGS=--warn-return-any --warn-unused-ignores --ignore-missing-imports \
--disallow-untyped-defs --check-untyped-defs \

# ----------------- #
#       Rules       #
# ----------------- #

.PHONY: all install run debug clean lint lint-strict lint-format


all: install run


install:
	@clear
	@if	! $(CHECK_UV) > /dev/null 2>&1; then \
			echo "UV not installed. Installing..."; \
			$(INSTALL_UV); \
	fi
	@echo "$(BROWN)Installing project dependencies using uv...$(END)"
	uv sync --link-mode=copy


run:
	@clear
	@echo "$(BLUE)Running the project...$(END)"
	$(PYTHON) -m src


debug:
	@clear
	@echo "$(BLUE)Running the project in debug...$(END)"
	$(PYTHON) -m pdb src $(JSON_FLAGS)


clean:
	@clear
	@echo "$(RED)Removing unecessary files from the folder...$(END)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -name "*.pyc" -delete
	rm -rf data/output
	@echo "\n$(GREEN)Folder cleaned!$(END)"


lint:
	@clear
	@status=0; \
	$(FLAKE8) src/ || status=$$?; \
	$(MYPY) src/ $(MYPY_FLAGS) || status=$$?; \
	exit $$status


lint-strict:
	@clear
	@status=0; \
	$(FLAKE8) src/ || status=$$?; \
	$(MYPY) src/ $(MYPY_FLAGS) --strict || status=$$?; \
	exit $$status

lint-format:
				uv run ruff format

# ----------------- #
#       Colors      #
# ----------------- #

BROWN=\e[1;33m
BLUE=\e[1;94m
RED=\e[1;31m
GREEN=\e[1;92m
END=\e[0m
