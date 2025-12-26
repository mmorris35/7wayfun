.PHONY: test lint format clean sim help

# Default target
help:
	@echo "trailer-tester development commands:"
	@echo ""
	@echo "  make test    - Run simulator tests"
	@echo "  make lint    - Check code with ruff"
	@echo "  make format  - Format code with ruff"
	@echo "  make sim     - Launch interactive simulator"
	@echo "  make clean   - Remove __pycache__ and .pyc files"
	@echo ""

# Run simulator tests
test:
	@echo "Running firmware tests..."
	@python3 simulator/test_firmware.py

# Lint code
lint:
	@echo "Checking code with ruff..."
	@ruff check firmware/ simulator/ || true

# Format code
format:
	@echo "Formatting code with ruff..."
	@ruff format firmware/ simulator/

# Launch interactive simulator
sim:
	@echo "Launching interactive simulator..."
	@python3 simulator/run_simulator.py

# Clean up Python cache files
clean:
	@echo "Cleaning up..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Done."

# Install development dependencies
install-dev:
	@echo "Installing development dependencies..."
	@pip install -e ".[dev]"
