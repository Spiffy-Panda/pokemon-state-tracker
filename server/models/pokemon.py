from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

class PokemonBaseStats(BaseModel):
    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

class PokemonAbility(BaseModel):
    name: str
    is_hidden: bool = False

class Pokemon(BaseModel):
    id: int
    name: str
    level: int
    types: List[str]
    abilities: List[PokemonAbility] = []
    nature: str
    held_item: Optional[str] = None
    base_stats: PokemonBaseStats
    current_hp: int
    max_hp: int
    gender: str = "Unknown"
    is_shiny: bool = False
    form: str = "Normal"

class PokemonCreate(BaseModel):
    name: str
    level: int
    types: List[str]
    abilities: List[PokemonAbility] = []
    nature: str = "Hardy"
    held_item: Optional[str] = None
    base_stats: Dict[str, int]
    gender: str = "Unknown"
    is_shiny: bool = False
    form: str = "Normal"
