from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from server.models.pokemon import Pokemon, PokemonCreate

class MapLocation(BaseModel):
    location_tuple: List[str]
    description: Optional[str] = None
    accessible_locations: List[List[str]] = []

class MapLocationCreate(BaseModel):
    location_tuple: List[str]
    description: Optional[str] = None
    accessible_locations: List[List[str]] = []

class Thought(BaseModel):
    content: str
    category: str = "general"  # general, battle, exploration
    timestamp: datetime = Field(default_factory=datetime.now)
    context: Optional[Dict[str, Any]] = None

class ThoughtCreate(BaseModel):
    content: str
    category: str = "general"  # general, battle, exploration
    context: Optional[Dict[str, Any]] = None

class MatchupRecord(BaseModel):
    opponent_id: str
    opponent_name: str
    wins: int = 0
    losses: int = 0
    draws: int = 0
    last_battle: Optional[datetime] = None

class Battle(BaseModel):
    id: str
    opponent_id: str
    opponent_name: str
    player_team: List[Pokemon] = []
    opponent_team: List[Pokemon] = []
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    result: Optional[str] = None  # win, loss, draw
    turns: List[Dict[str, Any]] = []

class BattleCreate(BaseModel):
    opponent_id: str
    opponent_name: str

class Player(BaseModel):
    id: str
    name: str
    team: List[Pokemon] = []
    location: MapLocation
    thought_history: List[Thought] = []
    battle_history: List[Battle] = []
    matchup_records: Dict[str, MatchupRecord] = {}
    items: List[str] = []
    badges: Set[str] = set()
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)

class PlayerCreate(BaseModel):
    name: str
    team: List[PokemonCreate] = []
    location: MapLocationCreate
    items: List[str] = []
    badges: List[str] = []

class PlayerUpdate(BaseModel):
    name: str
    location: MapLocationCreate
    items: List[str] = []
    badges: List[str] = []
