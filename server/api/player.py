from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import datetime

from server.models.player import Player, PlayerCreate, PlayerUpdate, ThoughtCreate, BattleCreate
from server.models.pokemon import Pokemon, PokemonCreate
from server.models.api import APIResponse

router = APIRouter(prefix="/players", tags=["players"])

# In-memory storage (would be replaced with a database in production)
players = {}

# Helper functions
def get_player(player_id: str) -> Player:
    if player_id not in players:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    return players[player_id]

def get_all_players() -> List[Player]:
    return list(players.values())

def replace_all_players(new_players: List[Player]) -> None:
    global players
    players = {player.id: player for player in new_players}

# Player endpoints
@router.post("/", response_model=APIResponse)
async def create_player(player: PlayerCreate):
    player_id = f"player_{len(players) + 1}"
    
    # Create new player
    new_player = Player(
        id=player_id,
        name=player.name,
        team=player.team,
        location=player.location,
        thought_history=[],
        battle_history=[],
        matchup_records={},
        created_at=datetime.datetime.now(),
        last_updated=datetime.datetime.now()
    )
    
    players[player_id] = new_player
    
    return {
        "success": True,
        "message": f"Player {player.name} created successfully",
        "data": {"player_id": player_id}
    }

@router.get("/", response_model=APIResponse)
async def list_players(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100)):
    player_list = list(players.values())
    total = len(player_list)
    total_pages = (total + per_page - 1) // per_page if total > 0 else 1
    
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total)
    
    paginated_players = player_list[start_idx:end_idx]
    
    return {
        "success": True,
        "message": f"Retrieved {len(paginated_players)} players",
        "data": paginated_players,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": total_pages
    }

@router.get("/{player_id}", response_model=APIResponse)
async def get_player_by_id(player_id: str):
    player = get_player(player_id)
    return {
        "success": True,
        "message": f"Retrieved player {player.name}",
        "data": player
    }

@router.put("/{player_id}", response_model=APIResponse)
async def update_player(player_id: str, player_update: PlayerUpdate):
    player = get_player(player_id)
    
    # Update player fields
    player.name = player_update.name
    player.location = player_update.location
    player.last_updated = datetime.datetime.now()
    
    return {
        "success": True,
        "message": f"Player {player.name} updated successfully",
        "data": player
    }

@router.delete("/{player_id}", response_model=APIResponse)
async def delete_player(player_id: str):
    if player_id not in players:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found")
    
    player_name = players[player_id].name
    del players[player_id]
    
    return {
        "success": True,
        "message": f"Player {player_name} deleted successfully"
    }

# Team management endpoints
@router.get("/{player_id}/team", response_model=APIResponse)
async def get_player_team(player_id: str):
    player = get_player(player_id)
    return {
        "success": True,
        "message": f"Retrieved team for player {player.name}",
        "data": {"team": player.team}
    }

@router.post("/{player_id}/team", response_model=APIResponse)
async def add_pokemon_to_team(player_id: str, pokemon: PokemonCreate):
    player = get_player(player_id)
    
    if len(player.team) >= 6:
        raise HTTPException(status_code=400, detail="Team already has maximum 6 Pokemon")
    
    # Create new Pokemon
    new_pokemon = Pokemon(
        id=len(player.team) + 1,
        name=pokemon.name,
        level=pokemon.level,
        types=pokemon.types,
        abilities=pokemon.abilities,
        nature=pokemon.nature,
        held_item=pokemon.held_item,
        base_stats=pokemon.base_stats,
        current_hp=pokemon.base_stats.hp,
        max_hp=pokemon.base_stats.hp
    )
    
    player.team.append(new_pokemon)
    player.last_updated = datetime.datetime.now()
    
    return {
        "success": True,
        "message": f"Added {pokemon.name} to {player.name}'s team",
        "data": new_pokemon
    }

@router.delete("/{player_id}/team/{pokemon_index}", response_model=APIResponse)
async def remove_team_pokemon(player_id: str, pokemon_index: int):
    player = get_player(player_id)
    
    if pokemon_index < 0 or pokemon_index >= len(player.team):
        raise HTTPException(status_code=404, detail=f"Pokemon at index {pokemon_index} not found")
    
    removed_pokemon = player.team.pop(pokemon_index)
    player.last_updated = datetime.datetime.now()
    
    return {
        "success": True,
        "message": f"Removed {removed_pokemon.name} from {player.name}'s team"
    }

# Thought history endpoints
@router.get("/{player_id}/thoughts", response_model=APIResponse)
async def get_player_thoughts(player_id: str):
    player = get_player(player_id)
    return {
        "success": True,
        "message": f"Retrieved thoughts for player {player.name}",
        "data": {"thoughts": player.thought_history}
    }

@router.post("/{player_id}/thoughts", response_model=APIResponse)
async def add_player_thought(player_id: str, thought: ThoughtCreate):
    player = get_player(player_id)
    
    # Create new thought
    thought_id = f"thought_{len(player.thought_history) + 1}"
    new_thought = {
        "id": thought_id,
        "content": thought.content,
        "category": thought.category,
        "timestamp": datetime.datetime.now()
    }
    
    player.thought_history.append(new_thought)
    player.last_updated = datetime.datetime.now()
    
    return {
        "success": True,
        "message": f"Added thought for player {player.name}",
        "data": new_thought
    }

# Battle history endpoints
@router.get("/{player_id}/battles", response_model=APIResponse)
async def get_player_battles(player_id: str):
    player = get_player(player_id)
    return {
        "success": True,
        "message": f"Retrieved battles for player {player.name}",
        "data": {"battles": player.battle_history}
    }

@router.post("/{player_id}/battles", response_model=APIResponse)
async def start_battle(player_id: str, battle: BattleCreate):
    player = get_player(player_id)
    
    # Create new battle
    battle_id = f"battle_{len(player.battle_history) + 1}"
    new_battle = {
        "id": battle_id,
        "opponent_id": battle.opponent_id,
        "opponent_name": battle.opponent_name,
        "start_time": datetime.datetime.now(),
        "end_time": None,
        "result": None,
        "player_team": player.team,
        "opponent_team": [],
        "turns": []
    }
    
    player.battle_history.append(new_battle)
    player.last_updated = datetime.datetime.now()
    
    return {
        "success": True,
        "message": f"Started battle against {battle.opponent_name}",
        "data": {"battle_id": battle_id}
    }

@router.get("/{player_id}/battles/{battle_id}", response_model=APIResponse)
async def get_battle_details(player_id: str, battle_id: str):
    player = get_player(player_id)
    
    # Find battle
    battle = next((b for b in player.battle_history if b["id"] == battle_id), None)
    if not battle:
        raise HTTPException(status_code=404, detail=f"Battle with ID {battle_id} not found")
    
    return {
        "success": True,
        "message": f"Retrieved battle details",
        "data": battle
    }

@router.put("/{player_id}/battles/{battle_id}", response_model=APIResponse)
async def end_battle(player_id: str, battle_id: str, result: str):
    player = get_player(player_id)
    
    # Find battle
    battle = next((b for b in player.battle_history if b["id"] == battle_id), None)
    if not battle:
        raise HTTPException(status_code=404, detail=f"Battle with ID {battle_id} not found")
    
    # Validate result
    if result not in ["win", "loss", "draw"]:
        raise HTTPException(status_code=400, detail=f"Invalid result: {result}. Must be 'win', 'loss', or 'draw'")
    
    # Update battle
    battle["result"] = result
    battle["end_time"] = datetime.datetime.now()
    
    # Update matchup records
    opponent_id = battle["opponent_id"]
    if opponent_id not in player.matchup_records:
        player.matchup_records[opponent_id] = {
            "opponent_id": opponent_id,
            "opponent_name": battle["opponent_name"],
            "wins": 0,
            "losses": 0,
            "draws": 0,
            "last_battle": datetime.datetime.now()
        }
    
    if result == "win":
        player.matchup_records[opponent_id]["wins"] += 1
    elif result == "loss":
        player.matchup_records[opponent_id]["losses"] += 1
    else:
        player.matchup_records[opponent_id]["draws"] += 1
    
    player.matchup_records[opponent_id]["last_battle"] = datetime.datetime.now()
    player.last_updated = datetime.datetime.now()
    
    return {
        "success": True,
        "message": f"Battle ended with result: {result}",
        "data": battle
    }

# Matchup records endpoints
@router.get("/{player_id}/matchups", response_model=APIResponse)
async def get_player_matchups(player_id: str):
    player = get_player(player_id)
    return {
        "success": True,
        "message": f"Retrieved matchup records for player {player.name}",
        "data": {"matchups": player.matchup_records}
    }
