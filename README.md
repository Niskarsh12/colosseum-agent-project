# Solana Yield Optimizer

A clean, deterministic prototype for optimizing yield strategies on Solana. This version introduces a deterministic audit trail for yield planning, allowing agents to prove their logic without exposing sensitive internal state.

## Features
- Deterministic yield calculation logic.
- Audit logging with state hashing (inspired by SlotScribe feedback).
- Zero external dependencies (Standard Library only).

## Running the Project
```cmd
python main.py
```

## Running Tests
```cmd
python -m unittest discover -s tests
```