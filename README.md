# Pokemon Player State Tracker

A comprehensive system for tracking Pokemon player state data for LLM-controlled players, featuring team management, map location tracking, thought history, match-up records, and battle history.

## Features

- **Player State Tracking**: Track player teams, locations, thoughts, battles, and matchups
- **RESTful API**: Full API for managing player state data
- **Web Inspector**: Visual interface for monitoring and managing player state
- **Save/Load Functionality**: Persist and restore player state data
- **Black 2/White 2 Rules**: Follows Pokemon Black 2 and White 2 game mechanics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pokemon-state-tracker.git
cd pokemon-state-tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Server

```bash
python -m server.main
```

The server will start on http://localhost:8000

### Web Interface

Access the web interface by opening a browser and navigating to:
- Home: http://localhost:8000/
- Players: http://localhost:8000/players
- Saves: http://localhost:8000/saves

### API Endpoints

#### Player Management
- `GET /players/`: List all players
- `POST /players/`: Create a new player
- `GET /players/{player_id}`: Get player details
- `PUT /players/{player_id}`: Update player
- `DELETE /players/{player_id}`: Delete player

#### Team Management
- `GET /players/{player_id}/team`: Get player's team
- `POST /players/{player_id}/team`: Add Pokemon to team
- `PUT /players/{player_id}/team/{pokemon_index}`: Update Pokemon
- `DELETE /players/{player_id}/team/{pokemon_index}`: Remove Pokemon

#### Thought History
- `GET /players/{player_id}/thoughts`: Get player's thoughts
- `POST /players/{player_id}/thoughts`: Add thought

#### Battle History
- `GET /players/{player_id}/battles`: Get player's battles
- `POST /players/{player_id}/battles`: Start new battle
- `GET /players/{player_id}/battles/{battle_id}`: Get battle details
- `PUT /players/{player_id}/battles/{battle_id}`: Update battle result

#### Matchup Records
- `GET /players/{player_id}/matchups`: Get player's matchup records

#### Save/Load Functionality
- `GET /saves/`: List all saves
- `POST /saves/`: Create new save
- `GET /saves/{save_id}`: Get save details
- `PUT /saves/{save_id}`: Update save
- `DELETE /saves/{save_id}`: Delete save
- `POST /saves/{save_id}/load`: Load save
- `POST /saves/{save_id}/backup`: Create backup

## Data Models

### Player
```json
{
  "id": "player_1",
  "name": "Ash",
  "team": [...],
  "location": {
    "location_tuple": ["Aspertia City", "Trainer School"],
    "description": "A school for beginning trainers",
    "accessible_locations": [...]
  },
  "thought_history": [...],
  "battle_history": [...],
  "matchup_records": {...},
  "items": ["Potion", "Pokeball"],
  "badges": []
}
```

### Pokemon
```json
{
  "id": 1,
  "name": "Oshawott",
  "level": 5,
  "types": ["Water"],
  "abilities": [{"name": "Torrent", "is_hidden": false}],
  "nature": "Modest",
  "held_item": null,
  "base_stats": {
    "hp": 55,
    "attack": 55,
    "defense": 45,
    "special_attack": 63,
    "special_defense": 45,
    "speed": 45
  },
  "current_hp": 55,
  "max_hp": 55
}
```

### Map Location
```json
{
  "location_tuple": ["Aspertia City", "Trainer School"],
  "description": "A school for beginning trainers",
  "accessible_locations": [
    ["Aspertia City", "Lookout"],
    ["Aspertia City", "Pokemon Center"]
  ]
}
```

### Thought
```json
{
  "id": "thought_1",
  "content": "I should challenge the gym leader",
  "category": "battle",
  "timestamp": "2025-03-20T12:34:56"
}
```

### Battle
```json
{
  "id": "battle_1",
  "opponent_id": "npc_1",
  "opponent_name": "Rival Hugh",
  "start_time": "2025-03-20T12:34:56",
  "end_time": "2025-03-20T12:45:23",
  "result": "win",
  "player_team": [...],
  "opponent_team": [...],
  "turns": [...]
}
```

### Save File
```json
{
  "id": "save_20250320123456",
  "name": "My Save",
  "game_version": "Black2White2",
  "created_at": "2025-03-20T12:34:56",
  "last_updated": "2025-03-20T13:45:23",
  "players": [...]
}
```

## Testing

Run the automated tests:

```bash
./run_tests.sh
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [PokeAPI](https://pokeapi.co/) for Pokemon data structure reference
- [Pokemon Showdown](https://github.com/smogon/pokemon-showdown) for battle mechanics reference
- [PokeCompanion](https://community.sambanova.ai/t/pokecompanion-your-pokemon-companion-rival-that-can-engage-in-battles-theory-crafting-and-team-building-lightning-hackathon/662) for implementation ideas
