import os
import json
import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from server.models.player import Player
from server.models.pokemon import Pokemon
from server.models.save import SaveFile, SaveFileCreate, SaveFileResponse, SaveFileList

# Directory for save files
SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "saves")

# Ensure save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

class SaveManager:
    """Manager for save/load functionality"""
    
    @staticmethod
    def get_save_path(save_id: str) -> str:
        """Get the file path for a save file"""
        return os.path.join(SAVE_DIR, f"{save_id}.json")
    
    @staticmethod
    def create_save(save_data: SaveFileCreate, players: List[Player]) -> SaveFile:
        """Create a new save file"""
        # Generate save ID
        save_id = f"save_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Create save file object
        save_file = SaveFile(
            id=save_id,
            name=save_data.name,
            game_version=save_data.game_version,
            created_at=datetime.datetime.now(),
            last_updated=datetime.datetime.now(),
            players=[player.dict() for player in players]
        )
        
        # Save to file
        with open(SaveManager.get_save_path(save_id), "w") as f:
            json.dump(save_file.dict(), f, default=str, indent=2)
        
        return save_file
    
    @staticmethod
    def get_all_saves() -> List[SaveFileResponse]:
        """Get all save files"""
        saves = []
        
        # Check if directory exists
        if not os.path.exists(SAVE_DIR):
            return saves
        
        # List all save files
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith(".json"):
                try:
                    with open(os.path.join(SAVE_DIR, filename), "r") as f:
                        save_data = json.load(f)
                        # Convert string dates to datetime objects
                        save_data["created_at"] = datetime.datetime.fromisoformat(save_data["created_at"].replace("Z", "+00:00"))
                        save_data["last_updated"] = datetime.datetime.fromisoformat(save_data["last_updated"].replace("Z", "+00:00"))
                        save_file = SaveFile(**save_data)
                        saves.append(SaveFileResponse(
                            id=save_file.id,
                            name=save_file.name,
                            game_version=save_file.game_version,
                            created_at=save_file.created_at,
                            last_updated=save_file.last_updated
                        ))
                except Exception as e:
                    print(f"Error loading save file {filename}: {e}")
        
        # Sort by last updated (newest first)
        saves.sort(key=lambda x: x.last_updated, reverse=True)
        
        return saves
    
    @staticmethod
    def get_save(save_id: str) -> Optional[SaveFile]:
        """Get a specific save file"""
        save_path = SaveManager.get_save_path(save_id)
        
        if not os.path.exists(save_path):
            return None
        
        try:
            with open(save_path, "r") as f:
                save_data = json.load(f)
                # Convert string dates to datetime objects
                save_data["created_at"] = datetime.datetime.fromisoformat(save_data["created_at"].replace("Z", "+00:00"))
                save_data["last_updated"] = datetime.datetime.fromisoformat(save_data["last_updated"].replace("Z", "+00:00"))
                return SaveFile(**save_data)
        except Exception as e:
            print(f"Error loading save file {save_id}: {e}")
            return None
    
    @staticmethod
    def delete_save(save_id: str) -> bool:
        """Delete a save file"""
        save_path = SaveManager.get_save_path(save_id)
        
        if not os.path.exists(save_path):
            return False
        
        try:
            os.remove(save_path)
            return True
        except Exception as e:
            print(f"Error deleting save file {save_id}: {e}")
            return False
    
    @staticmethod
    def load_save(save_id: str) -> Optional[List[Player]]:
        """Load players from a save file"""
        save_file = SaveManager.get_save(save_id)
        
        if not save_file:
            return None
        
        try:
            # Convert player dictionaries to Player objects
            players = []
            for player_data in save_file.players:
                # Convert Pokemon dictionaries to Pokemon objects
                team = []
                for pokemon_data in player_data["team"]:
                    pokemon = Pokemon(
                        id=pokemon_data["id"],
                        name=pokemon_data["name"],
                        level=pokemon_data["level"],
                        types=pokemon_data["types"],
                        abilities=pokemon_data["abilities"],
                        nature=pokemon_data["nature"],
                        held_item=pokemon_data["held_item"],
                        base_stats=pokemon_data["base_stats"],
                        current_hp=pokemon_data["current_hp"],
                        max_hp=pokemon_data["max_hp"],
                        gender=pokemon_data["gender"],
                        is_shiny=pokemon_data["is_shiny"],
                        form=pokemon_data["form"]
                    )
                    team.append(pokemon)
                
                # Create player object
                player = Player(
                    id=player_data["id"],
                    name=player_data["name"],
                    team=team,
                    location=player_data["location"],
                    thought_history=player_data["thought_history"],
                    battle_history=player_data["battle_history"],
                    matchup_records=player_data["matchup_records"],
                    items=player_data["items"],
                    badges=set(player_data["badges"]),
                    created_at=datetime.datetime.fromisoformat(player_data["created_at"].replace("Z", "+00:00")),
                    last_updated=datetime.datetime.fromisoformat(player_data["last_updated"].replace("Z", "+00:00"))
                )
                
                players.append(player)
            
            return players
        except Exception as e:
            print(f"Error loading players from save file {save_id}: {e}")
            return None
    
    @staticmethod
    def update_save(save_id: str, players: List[Player]) -> Optional[SaveFile]:
        """Update an existing save file with new player data"""
        save_file = SaveManager.get_save(save_id)
        
        if not save_file:
            return None
        
        try:
            # Update player data and last_updated timestamp
            save_file.players = [player.dict() for player in players]
            save_file.last_updated = datetime.datetime.now()
            
            # Save to file
            with open(SaveManager.get_save_path(save_id), "w") as f:
                json.dump(save_file.dict(), f, default=str, indent=2)
            
            return save_file
        except Exception as e:
            print(f"Error updating save file {save_id}: {e}")
            return None
    
    @staticmethod
    def create_backup(save_id: str) -> Optional[str]:
        """Create a backup of a save file"""
        save_path = SaveManager.get_save_path(save_id)
        
        if not os.path.exists(save_path):
            return None
        
        try:
            # Generate backup filename with timestamp
            backup_id = f"{save_id}_backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
            backup_path = SaveManager.get_save_path(backup_id)
            
            # Copy save file to backup
            with open(save_path, "r") as src, open(backup_path, "w") as dst:
                dst.write(src.read())
            
            return backup_id
        except Exception as e:
            print(f"Error creating backup of save file {save_id}: {e}")
            return None
