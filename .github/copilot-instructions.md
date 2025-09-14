# Copilot Coding Agent Onboarding Instructions

## High-Level Repository Overview

- **Project Name:** PhotoSort
- **Purpose:** Command-line tool to organize large collections of photos and videos by date and location, using metadata. Also provides a scan report of files.
- **Languages:** Python 3.9–3.11
- **Frameworks/Tools:** Poetry (dependency management), Pytest (testing), Black (formatting), Pylint (linting), Mypy (type checking), Coverage (test coverage)
- **Containerization:** Docker/Docker Compose supported
- **Repo Size:** Medium; main code in `photosort/` with modular subfolders for features.

## Build, Test, and Validation Instructions

### Environment Setup

- **Always use Poetry for dependency management.**
- **Python version:** `>=3.9,<3.12` (prefer Python 3.11 for Docker)
- **Install dependencies:**  
  ```bash
  poetry install
  ```
- **Optional:** Use Docker for isolated builds:
  ```bash
  docker build -t photosort .
  docker run --rm -v $(pwd)/photos:/photos photosort
  ```

### Linting & Type Checking

- **Run all lint/type checks before submitting changes:**
  ```bash
  ./lint.sh
  ```
  - Runs Black, Pylint, and Mypy on `photosort/`
  - **Precondition:** Poetry environment must be set up.

### Testing

- **Run all tests with coverage:**
  ```bash
  ./test.sh
  ```
  - Uses Pytest, outputs coverage to terminal and `htmlcov/index.html`
  - **Precondition:** Poetry environment must be set up.
  - **Test location:** All tests in `photosort/tests/`
  - **Minimal stub test present; add real tests for new features.**

### Running the Application

- **CLI entry point:**  
  ```bash
  poetry run python -m photosort.main
  ```
- **Docker Compose:**  
  ```bash
  docker-compose up --build
  ```
  - Mounts `./photos` as volume for input/output.

### Cleaning & Troubleshooting

- **If you encounter dependency or environment issues:**
  - Run `poetry install` again.
  - Remove `.venv` and re-create if needed.
  - For Docker, rebuild with `docker-compose build`.

### Validation Steps

- **Always run lint and tests before submitting.**
- **Check coverage report for missing test coverage.**
- **Validate CLI runs without error.**
- **Check logs for errors (JSON format).**

## Project Layout & Architecture

- **Root files:**  
  - `README.md` (project spec)
  - `Dockerfile`, `docker-compose.yml` (containerization)
  - `pyproject.toml`, `poetry.lock` (dependencies)
  - `lint.sh`, `test.sh` (scripts)
- **Main code:**  
  - `photosort/`
    - `main.py` (CLI entry)
    - `logging/` (JSON logging)
    - `organizer/` (file sorting/moving)
    - `scanner/` (metadata scanning)
    - `metadata/` (EXIF/video metadata extraction)
    - `utils/` (progress bar, batch utilities)
    - `tests/` (unit tests)
- **Configuration:**  
  - Linting: `lint.sh`
  - Testing: `test.sh`
  - Poetry: `pyproject.toml`
- **No GitHub Actions or CI/CD workflows present.**  
  - **Agent should run all local validation steps before proposing changes.**

## Key Facts & Best Practices

- **All logs and reports are in JSON format.**
- **Supported file types:** `.jpg`, `.png`, `.mp4`, `.mov`, `.heic`, `.avi`, `.gif`
- **Folder structure for sorted files:** `YYYY/YYYY-MM/YYYY-MM-DD[-location]/`
- **On filename conflict:** append counter (e.g., `IMG_001_1.jpg`)
- **No content-based duplicate checking.**
- **Dry run mode supported (preview changes).**
- **Error handling:** log errors, do not halt execution.
- **Initial scan outputs summary to JSON file.**

## Trust These Instructions

- **Trust these instructions for build, test, and validation.**
- **Only perform additional searches if these instructions are incomplete or found to be in error.**
- **Document any new errors or workarounds in this file for future agents.**

---

Place this file at `.github/copilot-instructions.md`. This will ensure Copilot agents work efficiently and reliably in the `photoSort` repository.
