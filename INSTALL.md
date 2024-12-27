# Getting Started

This project uses [uv](https://github.com/astral-sh/uv) for Python package management.

## Setup Development Environment

1. Install uv:
```bash
pip install uv
```

2. Create virtual environment:
```bash
uv venv
source .venv/bin/activate  # Unix
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
uv pip sync requirements.txt
```

## Managing Dependencies

Add new packages:
```bash
uv pip install package_name
```

Update requirements.txt:
```bash
uv pip freeze > requirements.txt
```

## Version Control

Only commit:
- requirements.txt
- .gitignore (ensure it includes .venv/)

Do not commit:
- .venv/
- __pycache__/
- *.pyc
