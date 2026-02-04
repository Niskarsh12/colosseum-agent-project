# Solana Pulse

A lightweight tool to monitor Solana network health and persist snapshots locally. Built for the Colosseum Agent Hackathon.

## Features
- **Poll**: Fetch health, slot, and blockhash from Solana Devnet.
- **Persist**: Save snapshots to `data/snapshots.json`.
- **Serve**: View a simple HTML dashboard on `http://localhost:8000`.

## Usage

### Single Snapshot
```bash
python main.py once
```

### Start Dashboard
```bash
python main.py serve
```

### Run Tests
```bash
python -m unittest discover -s tests
```

## Safety Note
This project uses public RPC endpoints. Never hardcode private keys or sensitive API keys in the source code. Use environment variables for any future secret integrations.