# Solana Yield Optimizer

A clean, deterministic prototype for optimizing yield across Solana protocols. This version focuses on a structured adapter pattern and safe strategy planning.

This build fetches **read-only** yield signals from public APIs (no transactions, no keys).
If a live API call fails, it falls back to mock values so the demo still runs.

## Requirements
- Windows OS
- Python 3.10+

## Running the Project
```cmd
python main.py
```

## Running Tests
```cmd
python -m unittest discover -s tests
```
