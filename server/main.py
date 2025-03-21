from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Optional
import os
import json
from datetime import datetime

# Import models
from server.models.pokemon import Pokemon, PokemonCreate
from server.models.player import (
    Player, PlayerCreate, MapLocation, MapLocationCreate, 
    Thought, ThoughtCreate, Battle, BattleCreate, MatchupRecord
)
from server.models.save import SaveFile, SaveFileCreate
from server.models.api import APIResponse, PaginatedResponse

# Create FastAPI app
app = FastAPI(
    title="Pokemon Player State Tracker",
    description="RESTful API for tracking Pokemon player state for LLM-controlled players",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (would be replaced with a database in production)
players = {}
save_files = {}

# Helper functions
def get_player(player_id: str) -> Player:
    if player_id not in players:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    return players[player_id]

# Routes
@app.get("/", response_model=APIResponse)
async def root():
    return APIResponse(
        success=True,
        message="Pokemon Player State Tracker API is running",
        data={"version": "1.0.0"}
    )

# Player endpoints
@app.post("/players/", response_model=APIResponse)
async def create_player(player: PlayerCreate):
    player_id = f"player_{len(players) + 1}"
    
    # Create location
    location = MapLocation(
        location_tuple=player.location.location_tuple,
        description=player.location.description,
        accessible_locations=player.location.accessible_locations
    )
    
    # Create Pokemon team
    team = []
    for pokemon_data in player.team:
        # This is simplified - in a real implementation, you'd fetch Pokemon data from a database
        # or external API based on the name, and then apply the customizations
        base_stats = pokemon_data.base_stats
        pokemon = Pokemon(
            id=len(team) + 1,
            name=pokemon_data.name,
            level=pokemon_data.level,
            types=pokemon_data.types,
            abilities=[],  # Would be populated from a database
            moves=[],      # Would be populated from a database
            base_stats=base_stats,
            current_stats=base_stats,  # Simplified
            nature=pokemon_data.nature,
            held_item=pokemon_data.held_item,
            current_hp=base_stats["hp"],
            max_hp=base_stats["hp"],
            gender=pokemon_data.gender,
            is_shiny=pokemon_data.is_shiny,
            form=pokemon_data.form
        )
        team.append(pokemon)
    
    # Create player
    new_player = Player(
        id=player_id,
        name=player.name,
        team=team,
        location=location,
        thought_history=[],
        battle_history=[],
        matchup_records={},
        items=player.items,
        badges=set(player.badges)
    )
    
    players[player_id] = new_player
    
    return APIResponse(
        success=True,
        message=f"Player {player.name} created successfully",
        data={"player_id": player_id}
    )

@app.get("/players/", response_model=PaginatedResponse)
async def list_players(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100)):
    player_list = list(players.values())
    total = len(player_list)
    total_pages = (total + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    paginated_players = player_list[start_idx:end_idx]
    
    return PaginatedResponse(
        success=True,
        message=f"Retrieved {len(paginated_players)} players",
        data=paginated_players,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@app.get("/players/{player_id}", response_model=APIResponse)
async def get_player_by_id(player_id: str):
    player = get_player(player_id)
    return APIResponse(
        success=True,
        message=f"Retrieved player {player.name}",
        data=player.dict()
    )

@app.put("/players/{player_id}", response_model=APIResponse)
async def update_player(player_id: str, player_update: PlayerCreate):
    player = get_player(player_id)
    
    # Update player fields
    player.name = player_update.name
    
    # Update location
    player.location = MapLocation(
        location_tuple=player_update.location.location_tuple,
        description=player_update.location.description,
        accessible_locations=player_update.location.accessible_locations
    )
    
    # Update items and badges
    player.items = player_update.items
    player.badges = set(player_update.badges)
    
    # Update last_updated timestamp
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Player {player.name} updated successfully",
        data=player.dict()
    )

@app.delete("/players/{player_id}", response_model=APIResponse)
async def delete_player(player_id: str):
    if player_id not in players:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    
    player_name = players[player_id].name
    del players[player_id]
    
    return APIResponse(
        success=True,
        message=f"Player {player_name} deleted successfully",
        data=None
    )

# Team management endpoints
@app.get("/players/{player_id}/team", response_model=APIResponse)
async def get_player_team(player_id: str):
    player = get_player(player_id)
    return APIResponse(
        success=True,
        message=f"Retrieved team for player {player.name}",
        data={"team": [pokemon.dict() for pokemon in player.team]}
    )

@app.post("/players/{player_id}/team", response_model=APIResponse)
async def add_pokemon_to_team(player_id: str, pokemon: PokemonCreate):
    player = get_player(player_id)
    
    if len(player.team) >= 6:
        raise HTTPException(status_code=400, detail="Team already has maximum 6 Pokemon")
    
    # Create new Pokemon
    base_stats = pokemon.base_stats
    new_pokemon = Pokemon(
        id=len(player.team) + 1,
        name=pokemon.name,
        level=pokemon.level,
        types=pokemon.types,
        abilities=[],  # Would be populated from a database
        moves=[],      # Would be populated from a database
        base_stats=base_stats,
        current_stats=base_stats,  # Simplified
        nature=pokemon.nature,
        held_item=pokemon.held_item,
        current_hp=base_stats["hp"],
        max_hp=base_stats["hp"],
        gender=pokemon.gender,
        is_shiny=pokemon.is_shiny,
        form=pokemon.form
    )
    
    player.team.append(new_pokemon)
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Added {pokemon.name} to {player.name}'s team",
        data=new_pokemon.dict()
    )

@app.put("/players/{player_id}/team/{pokemon_index}", response_model=APIResponse)
async def update_team_pokemon(player_id: str, pokemon_index: int, pokemon_update: PokemonCreate):
    player = get_player(player_id)
    
    if pokemon_index < 0 or pokemon_index >= len(player.team):
        raise HTTPException(status_code=404, detail=f"Pokemon at index {pokemon_index} not found")
    
    # Update Pokemon
    base_stats = pokemon_update.base_stats
    player.team[pokemon_index] = Pokemon(
        id=player.team[pokemon_index].id,
        name=pokemon_update.name,
        level=pokemon_update.level,
        types=pokemon_update.types,
        abilities=[],  # Would be populated from a database
        moves=[],      # Would be populated from a database
        base_stats=base_stats,
        current_stats=base_stats,  # Simplified
        nature=pokemon_update.nature,
        held_item=pokemon_update.held_item,
        current_hp=base_stats["hp"],
        max_hp=base_stats["hp"],
        gender=pokemon_update.gender,
        is_shiny=pokemon_update.is_shiny,
        form=pokemon_update.form
    )
    
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Updated {pokemon_update.name} in {player.name}'s team",
        data=player.team[pokemon_index].dict()
    )

@app.delete("/players/{player_id}/team/{pokemon_index}", response_model=APIResponse)
async def remove_team_pokemon(player_id: str, pokemon_index: int):
    player = get_player(player_id)
    
    if pokemon_index < 0 or pokemon_index >= len(player.team):
        raise HTTPException(status_code=404, detail=f"Pokemon at index {pokemon_index} not found")
    
    removed_pokemon = player.team.pop(pokemon_index)
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Removed {removed_pokemon.name} from {player.name}'s team",
        data=None
    )

# Location tracking endpoints
@app.get("/players/{player_id}/location", response_model=APIResponse)
async def get_player_location(player_id: str):
    player = get_player(player_id)
    return APIResponse(
        success=True,
        message=f"Retrieved location for player {player.name}",
        data=player.location.dict()
    )

@app.put("/players/{player_id}/location", response_model=APIResponse)
async def update_player_location(player_id: str, location: MapLocationCreate):
    player = get_player(player_id)
    
    player.location = MapLocation(
        location_tuple=location.location_tuple,
        description=location.description,
        accessible_locations=location.accessible_locations
    )
    
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Updated location for player {player.name}",
        data=player.location.dict()
    )

# Thought history endpoints
@app.get("/players/{player_id}/thoughts", response_model=APIResponse)
async def get_player_thoughts(
    player_id: str, 
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1, le=100),
    category: Optional[str] = None
):
    player = get_player(player_id)
    
    # Filter by category if provided
    thoughts = player.thought_history
    if category:
        thoughts = [t for t in thoughts if t.category == category]
    
    # Sort by timestamp (newest first)
    thoughts = sorted(thoughts, key=lambda t: t.timestamp, reverse=True)
    
    # Paginate
    total = len(thoughts)
    total_pages = (total + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    paginated_thoughts = thoughts[start_idx:end_idx]
    
    return APIResponse(
        success=True,
        message=f"Retrieved {len(paginated_thoughts)} thoughts for player {player.name}",
        data={
            "thoughts": [t.dict() for t in paginated_thoughts],
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages
            }
        }
    )

@app.post("/players/{player_id}/thoughts", response_model=APIResponse)
async def add_player_thought(player_id: str, thought: ThoughtCreate):
    player = get_player(player_id)
    
    new_thought = Thought(
        content=thought.content,
        category=thought.category,
        context=thought.context
    )
    
    player.thought_history.append(new_thought)
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Added thought for player {player.name}",
        data=new_thought.dict()
    )

# Battle history endpoints
@app.get("/players/{player_id}/battles", response_model=APIResponse)
async def get_player_battles(
    player_id: str, 
    page: int = Query(1, ge=1), 
    per_page: int = Query(10, ge=1, le=100),
    opponent_id: Optional[str] = None
):
    player = get_player(player_id)
    
    # Filter by opponent if provided
    battles = player.battle_history
    if opponent_id:
        battles = [b for b in battles if b.opponent_id == opponent_id]
    
    # Sort by start_time (newest first)
    battles = sorted(battles, key=lambda b: b.start_time, reverse=True)
    
    # Paginate
    total = len(battles)
    total_pages = (total + per_page - 1) // per_page
    
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    paginated_battles = battles[start_idx:end_idx]
    
    return APIResponse(
        success=True,
        message=f"Retrieved {len(paginated_battles)} battles for player {player.name}",
        data={
            "battles": [b.dict() for b in paginated_battles],
            "pagination": {
                "total": total,
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages
            }
        }
    )

@app.post("/players/{player_id}/battles", response_model=APIResponse)
async def add_player_battle(player_id: str, battle: BattleCreate):
    player = get_player(player_id)
    
    battle_id = f"battle_{len(player.battle_history) + 1}"
    
    new_battle = Battle(
        id=battle_id,
        opponent_id=battle.opponent_id,
        opponent_name=battle.opponent_name,
        player_team=player.team,  # Use current team
        opponent_team=[]  # Will be populated during battle
    )
    
    player.battle_history.append(new_battle)
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Started battle for player {player.name} against {battle.opponent_name}",
        data={"battle_id": battle_id}
    )

@app.get("/players/{player_id}/battles/{battle_id}", response_model=APIResponse)
async def get_battle_by_id(player_id: str, battle_id: str):
    player = get_player(player_id)
    
    battle = next((b for b in player.battle_history if b.id == battle_id), None)
    if not battle:
        raise HTTPException(status_code=404, detail=f"Battle with ID {battle_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Retrieved battle {battle_id}",
        data=battle.dict()
    )

@app.put("/players/{player_id}/battles/{battle_id}", response_model=APIResponse)
async def update_battle(player_id: str, battle_id: str, result: str):
    player = get_player(player_id)
    
    battle = next((b for b in player.battle_history if b.id == battle_id), None)
    if not battle:
        raise HTTPException(status_code=404, detail=f"Battle with ID {battle_id} not found")
    
    # Update battle result
    battle.result = result
    battle.end_time = datetime.now()
    
    # Update matchup record
    if battle.opponent_id not in player.matchup_records:
        player.matchup_records[battle.opponent_id] = MatchupRecord(
            opponent_id=battle.opponent_id,
            opponent_name=battle.opponent_name
        )
    
    record = player.matchup_records[battle.opponent_id]
    if result == "win":
        record.wins += 1
    elif result == "loss":
        record.losses += 1
    elif result == "draw":
        record.draws += 1
    
    record.last_battle = datetime.now()
    player.last_updated = datetime.now()
    
    return APIResponse(
        success=True,
        message=f"Updated battle {battle_id} with result: {result}",
        data=battle.dict()
    )

# Matchup record endpoints
@app.get("/players/{player_id}/matchups", response_model=APIResponse)
async def get_player_matchups(player_id: str):
    player = get_player(player_id)
    
    return APIResponse(
        success=True,
        message=f"Retrieved matchup records for player {player.name}",
        data={"matchups": {k: v.dict() for k, v in player.matchup_records.items()}}
    )

@app.get("/players/{player_id}/matchups/{opponent_id}", response_model=APIResponse)
async def get_specific_matchup(player_id: str, opponent_id: str):
    player = get_player(player_id)
    
    if opponent_id not in player.matchup_records:
        raise HTTPException(status_code=404, detail=f"Matchup record with opponent {opponent_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Retrieved matchup record with opponent {opponent_id}",
        data=player.matchup_records[opponent_id].dict()
    )

# Save/load endpoints
@app.post("/saves/", response_model=APIResponse)
async def create_save(save: SaveFileCreate):
    save_id = f"save_{len(save_files) + 1}"
    
    # Create a snapshot of all players
    data = {player_id: player.dict() for player_id, player in players.items()}
    
    new_save = SaveFile(
        id=save_id,
        name=save.name,
        data=data,
        game_version=save.game_version
    )
    
    save_files[save_id] = new_save
    
    return APIResponse(
        success=True,
        message=f"Created save file: {save.name}",
        data={"save_id": save_id}
    )

@app.get("/saves/", response_model=APIResponse)
async def list_saves():
    return APIResponse(
        success=True,
        message=f"Retrieved {len(save_files)} save files",
        data={"saves": [save.dict() for save in save_files.values()]}
    )

@app.get("/saves/{save_id}", response_model=APIResponse)
async def get_save(save_id: str):
    if save_id not in save_files:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found")
    
    return APIResponse(
        success=True,
        message=f"Retrieved save file: {save_files[save_id].name}",
        data=save_files[save_id].dict()
    )

@app.post("/saves/{save_id}/load", response_model=APIResponse)
async def load_save(save_id: str):
    if save_id not in save_files:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found")
    
    save = save_files[save_id]
    
    # Load player data from save file
    # In a real implementation, you would deserialize the data properly
    # This is a simplified version
    global players
    players = save.data
    
    return APIResponse(
        success=True,
        message=f"Loaded save file: {save.name}",
        data=None
    )

@app.delete("/saves/{save_id}", response_model=APIResponse)
async def delete_save(save_id: str):
    if save_id not in save_files:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found")
    
    save_name = save_files[save_id].name
    del save_files[save_id]
    
    return APIResponse(
        success=True,
        message=f"Deleted save file: {save_name}",
        data=None
    )

# Run the server
if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
