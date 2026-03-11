# The Hearth

The Hearth is a psychology-informed behavioral addiction tool.
It helps users identify what they are feeling and what unmet needs they may be medicating through compulsive behavior.
The approach is trauma-informed and focuses on unmet needs rather than surface level behavior.

## Psychology Frameworks

- **Cowen & Keltner's 27-category emotion taxonomy** — an empirically validated model of human emotion used for daily check-ins
- **ACT Urge Surfing** — an Acceptance and Commitment Therapy technique for riding out cravings without acting on them
- **NVC Needs Inventory** — Marshall Rosenberg's Nonviolent Communication framework used to identify unmet psychological needs underlying compulsive behavior

## Features

- Daily emotion and needs check-in based on Cowen & Keltner's 27 emotions
- Total day log
- Urge surfing assistant to help ride out cravings in real time
- Craving intensity visualizations over time

## Security

- This application uses bcrypt for secure password hashing. 
- When a user creates an account, their password is hashed with a unique salt before being stored in the database. 
- During login, the entered password is hashed and compared to the stored hash, ensuring that plaintext passwords are never stored or transmitted.
- db.py uses ? placeholders in every query to prevent SQL Injection
- All data is stored locally in SQLite with no network exposure for V1

## Installation
```
pip install rich matplotlib bcrypt pandas
```

## Running the App
```
python main.py
```
## Roadmap

- ~~Data exporting to CSV~~ - complete
- ~~FastAPI backend~~ - complete
- JWT authentication and brute force lockout
- Structured audit logging
- PostgreSQL migration
- Docker containerization
- GitHub Actions CI/CD pipeline
- React frontend for easy to use UI
- ML relapse prediction

## Important Note

This tool is not a diagnostic instrument and does not provide professional mental health treatment.
It is intended to support mindfulness around personal needs and emotional patterns only.
It is scoped to behavioral addictions with no physical withdrawal risk.

If you are experiencing a mental health crisis or thoughts of self-harm, call or text 988 (US).
