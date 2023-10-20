# Fantasy Football Snapshot Generator

This project generates a snapshot of ongoing fantasy football matchups by calculating the
remaining game time and current scores for live players in each matchup.
The snapshot is then stored for further usage and analysis.
The application uses data from the ESPN API and can handle live game statuses, including pre-game, in-game, and post-game states.

## How to Use

### Dependencies

I recommend using a `venv`. Install dependencies with:

```bash
pip install -r requirements.txt
```

### Prerequisites

Ensure that necessary environment variables are set:

- `LEAGUE_ID`: Your ESPN fantasy football league ID.
- `ESPN_S2`: Your ESPN S2 authentication token.
- `SWID`: Your SWID authentication token.
- `REDIS_URL`: Your Redis URL if you're using Redis for storage.

### Execution

Run the `main.py` file to generate and store a snapshot of the current matchups:

```bash
python main.py
```

## Output

The application will generate snapshots containing:

- The team IDs and names
- Time remaining for live players
- Current scores of the teams

These snapshots are stored and managed for further usage or analysis.
