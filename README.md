# Lab 22: Automating Business Workflows with Python

This folder contains the cleaned Lab 22 implementation for business workflow automation.

## Python files

- `workflow_auto.py` — main API → CSV → simulated email workflow
- `test_api.py` — API connectivity test
- `test_csv.py` — CSV creation test
- `analyze_results.py` — generated workflow data analysis
- `workflow_auto_enhanced.py` — enhanced workflow with retry, validation, cleaning, metadata, and reports
- `workflow_scheduler.py` — scheduler implementation using the `schedule` package
- `simple_scheduler.py` — simple scheduler demonstration

All Python `#` comments have been removed as requested. Python docstrings are retained because they are string literals, not comments.

## Setup

```bash
pip3 install -r requirements.txt
```

## Run

```bash
python3 workflow_auto.py
python3 workflow_auto_enhanced.py
python3 test_api.py
python3 test_csv.py
python3 analyze_results.py
python3 simple_scheduler.py
```

The email step in the provided lab is simulated and does not send a real email.
