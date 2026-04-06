# Contributing to vllm-embedding-api

Thank you for considering a contribution! This guide explains how to get set up, what conventions to follow, and how to submit your work.

---

## Table of contents

1. [Getting started](#getting-started)
2. [Development setup](#development-setup)
3. [Running tests](#running-tests)
4. [Code style](#code-style)
5. [Submitting a pull request](#submitting-a-pull-request)
6. [Reporting bugs & requesting features](#reporting-bugs--requesting-features)

---

## Getting started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/vllm-embedding-api.git
   cd vllm-embedding-api
   ```
3. Add the upstream remote so you can keep your fork in sync:
   ```bash
   git remote add upstream https://github.com/ThuanNaN/vllm-embedding-api.git
   ```

---

## Development setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install all dependencies (runtime + dev/test)
pip install -r requirements-dev.txt
```

Copy the environment template and fill it in:

```bash
cp .env.example .env
# Edit .env and set API_KEY (and optionally MODEL_NAME)
```

---

## Running tests

Tests mock the vLLM backend, so **no GPU is required** to run them.

```bash
python -m pytest tests/ -v
```

Please ensure all existing tests pass and add new tests for any functionality you introduce or change.

---

## Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use [type annotations](https://peps.python.org/pep-0484/) for all public functions and methods.
- Keep docstrings consistent with the style used in the existing codebase.
- Do not commit secrets, credentials, or personal data.

---

## Submitting a pull request

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/my-feature
   ```
2. Make your changes and commit them with a clear message:
   ```bash
   git commit -m "feat: add support for XYZ"
   ```
3. Keep your branch up to date with upstream:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```
4. Push to your fork and open a pull request against `ThuanNaN/vllm-embedding-api`'s `main` branch.
5. Fill in the pull-request template (if present) and describe **what** changed and **why**.
6. A maintainer will review your PR. Please address any feedback promptly.

---

## Reporting bugs & requesting features

- **Bug reports** – open a GitHub Issue and include steps to reproduce, expected behaviour, and actual behaviour.
- **Feature requests** – open a GitHub Issue describing the use case and the proposed solution.

We appreciate clear, concise issues with as much context as possible!
