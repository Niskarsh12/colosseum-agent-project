# Solana Yield Optimizer (Agent-built)

A minimal prototype for monitoring Solana devnet and planning yield allocations.

## Usage
- `python main.py once`: Fetch Solana RPC health/slot and save snapshot.
- `python main.py plan`: Generate allocation plan based on snapshots and strategy.
- `python main.py serve`: Start a local dashboard at http://localhost:8000

## Testing
`python -m unittest discover -s tests`