from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
import datetime

from server.utils.save_manager import SaveManager
from server.models.save import SaveFileCreate, SaveFileResponse, SaveFileList
from server.models.api import APIResponse
from server.api.player import get_all_players, replace_all_players

router = APIRouter(prefix="/saves", tags=["saves"])

@router.get("/", response_model=APIResponse)
async def get_saves():
    """Get all save files"""
    saves = SaveManager.get_all_saves()
    return {
        "success": True,
        "message": "Save files retrieved successfully",
        "data": {
            "saves": saves
        }
    }

@router.post("/", response_model=APIResponse)
async def create_save(save_data: SaveFileCreate):
    """Create a new save file"""
    # Get all current players
    players = get_all_players()
    
    # Create save file
    save_file = SaveManager.create_save(save_data, players)
    
    return {
        "success": True,
        "message": f"Save file '{save_data.name}' created successfully",
        "data": save_file
    }

@router.get("/{save_id}", response_model=APIResponse)
async def get_save(save_id: str):
    """Get a specific save file"""
    save_file = SaveManager.get_save(save_id)
    
    if not save_file:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found")
    
    return {
        "success": True,
        "message": "Save file retrieved successfully",
        "data": save_file
    }

@router.delete("/{save_id}", response_model=APIResponse)
async def delete_save(save_id: str):
    """Delete a save file"""
    success = SaveManager.delete_save(save_id)
    
    if not success:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found")
    
    return {
        "success": True,
        "message": f"Save file with ID {save_id} deleted successfully"
    }

@router.post("/{save_id}/load", response_model=APIResponse)
async def load_save(save_id: str):
    """Load a save file"""
    players = SaveManager.load_save(save_id)
    
    if not players:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found or could not be loaded")
    
    # Replace all current players with loaded players
    replace_all_players(players)
    
    return {
        "success": True,
        "message": f"Save file with ID {save_id} loaded successfully"
    }

@router.post("/{save_id}/backup", response_model=APIResponse)
async def create_backup(save_id: str):
    """Create a backup of a save file"""
    backup_id = SaveManager.create_backup(save_id)
    
    if not backup_id:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found or could not be backed up")
    
    return {
        "success": True,
        "message": f"Backup of save file with ID {save_id} created successfully",
        "data": {
            "backup_id": backup_id
        }
    }

@router.put("/{save_id}", response_model=APIResponse)
async def update_save(save_id: str):
    """Update a save file with current player data"""
    # Get all current players
    players = get_all_players()
    
    # Update save file
    save_file = SaveManager.update_save(save_id, players)
    
    if not save_file:
        raise HTTPException(status_code=404, detail=f"Save file with ID {save_id} not found")
    
    return {
        "success": True,
        "message": f"Save file with ID {save_id} updated successfully",
        "data": save_file
    }
