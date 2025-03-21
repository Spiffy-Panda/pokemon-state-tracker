import unittest
import requests
import json
import os
import sys
import time
from typing import Dict, List, Any

# Set the base URL for the API
BASE_URL = "http://localhost:8000/api"

class PokemonPlayerStateTrackerTest(unittest.TestCase):
    """Test cases for the Pokemon Player State Tracker API"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a test player
        self.test_player = {
            "name": "Test Trainer",
            "location": {
                "location_tuple": ["Aspertia City", "Trainer School"],
                "description": "A school for beginning trainers",
                "accessible_locations": [
                    ["Aspertia City", "Lookout"],
                    ["Aspertia City", "Pokemon Center"]
                ]
            },
            "team": [
                {
                    "name": "Oshawott",
                    "level": 5,
                    "types": ["Water"],
                    "abilities": [{"name": "Torrent", "is_hidden": False}],
                    "nature": "Modest",
                    "held_item": None,
                    "gender": "Male",
                    "is_shiny": False,
                    "form": "Normal",
                    "base_stats": {
                        "hp": 55,
                        "attack": 55,
                        "defense": 45,
                        "special_attack": 63,
                        "special_defense": 45,
                        "speed": 45
                    }
                }
            ],
            "items": ["Potion", "Pokeball"],
            "badges": []
        }
        
        # Create a test save
        self.test_save = {
            "name": "Test Save",
            "game_version": "Black2White2"
        }
        
        # Store created resources for cleanup
        self.created_resources = {
            "players": [],
            "saves": []
        }
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Delete created players
        for player_id in self.created_resources["players"]:
            try:
                requests.delete(f"{BASE_URL}/players/{player_id}")
            except:
                pass
        
        # Delete created saves
        for save_id in self.created_resources["saves"]:
            try:
                requests.delete(f"{BASE_URL}/saves/{save_id}")
            except:
                pass
    
    def test_api_root(self):
        """Test the API root endpoint"""
        response = requests.get(f"{BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("version", data["data"])
    
    def test_player_crud(self):
        """Test player CRUD operations"""
        # Create player
        response = requests.post(f"{BASE_URL}/players/", json=self.test_player)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        player_id = data["data"]["player_id"]
        self.created_resources["players"].append(player_id)
        
        # Get player
        response = requests.get(f"{BASE_URL}/players/{player_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["name"], self.test_player["name"])
        
        # Update player
        updated_player = self.test_player.copy()
        updated_player["name"] = "Updated Trainer"
        response = requests.put(f"{BASE_URL}/players/{player_id}", json=updated_player)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify update
        response = requests.get(f"{BASE_URL}/players/{player_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["data"]["name"], "Updated Trainer")
        
        # Delete player
        response = requests.delete(f"{BASE_URL}/players/{player_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify deletion
        response = requests.get(f"{BASE_URL}/players/{player_id}")
        self.assertEqual(response.status_code, 404)
        
        # Remove from cleanup list since we already deleted it
        self.created_resources["players"].remove(player_id)
    
    def test_team_management(self):
        """Test team management operations"""
        # Create player
        response = requests.post(f"{BASE_URL}/players/", json=self.test_player)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        player_id = data["data"]["player_id"]
        self.created_resources["players"].append(player_id)
        
        # Get team
        response = requests.get(f"{BASE_URL}/players/{player_id}/team")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]["team"]), 1)
        
        # Add Pokemon to team
        new_pokemon = {
            "name": "Tepig",
            "level": 5,
            "types": ["Fire"],
            "abilities": [{"name": "Blaze", "is_hidden": False}],
            "nature": "Adamant",
            "held_item": None,
            "gender": "Male",
            "is_shiny": False,
            "form": "Normal",
            "base_stats": {
                "hp": 65,
                "attack": 63,
                "defense": 45,
                "special_attack": 45,
                "special_defense": 45,
                "speed": 45
            }
        }
        
        response = requests.post(f"{BASE_URL}/players/{player_id}/team", json=new_pokemon)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify team size
        response = requests.get(f"{BASE_URL}/players/{player_id}/team")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["data"]["team"]), 2)
        
        # Update Pokemon
        updated_pokemon = new_pokemon.copy()
        updated_pokemon["level"] = 10
        response = requests.put(f"{BASE_URL}/players/{player_id}/team/1", json=updated_pokemon)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify update
        response = requests.get(f"{BASE_URL}/players/{player_id}/team")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["data"]["team"][1]["level"], 10)
        
        # Remove Pokemon
        response = requests.delete(f"{BASE_URL}/players/{player_id}/team/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify team size
        response = requests.get(f"{BASE_URL}/players/{player_id}/team")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["data"]["team"]), 1)
    
    def test_thought_history(self):
        """Test thought history operations"""
        # Create player
        response = requests.post(f"{BASE_URL}/players/", json=self.test_player)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        player_id = data["data"]["player_id"]
        self.created_resources["players"].append(player_id)
        
        # Add thought
        thought = {
            "content": "I should challenge the gym leader",
            "category": "battle"
        }
        
        response = requests.post(f"{BASE_URL}/players/{player_id}/thoughts", json=thought)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Get thoughts
        response = requests.get(f"{BASE_URL}/players/{player_id}/thoughts")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]["thoughts"]), 1)
        self.assertEqual(data["data"]["thoughts"][0]["content"], thought["content"])
    
    def test_battle_history(self):
        """Test battle history operations"""
        # Create player
        response = requests.post(f"{BASE_URL}/players/", json=self.test_player)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        player_id = data["data"]["player_id"]
        self.created_resources["players"].append(player_id)
        
        # Start battle
        battle = {
            "opponent_id": "npc_1",
            "opponent_name": "Rival Hugh"
        }
        
        response = requests.post(f"{BASE_URL}/players/{player_id}/battles", json=battle)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        battle_id = data["data"]["battle_id"]
        
        # Get battles
        response = requests.get(f"{BASE_URL}/players/{player_id}/battles")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(len(data["data"]["battles"]), 1)
        self.assertEqual(data["data"]["battles"][0]["opponent_name"], battle["opponent_name"])
        
        # End battle with result
        response = requests.put(f"{BASE_URL}/players/{player_id}/battles/{battle_id}", json="win")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify battle result
        response = requests.get(f"{BASE_URL}/players/{player_id}/battles/{battle_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["result"], "win")
    
    def test_save_load_functionality(self):
        """Test save/load functionality"""
        # Create player
        response = requests.post(f"{BASE_URL}/players/", json=self.test_player)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        player_id = data["data"]["player_id"]
        self.created_resources["players"].append(player_id)
        
        # Create save
        response = requests.post(f"{BASE_URL}/saves/", json=self.test_save)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        save_id = data["data"]["id"]
        self.created_resources["saves"].append(save_id)
        
        # Get saves
        response = requests.get(f"{BASE_URL}/saves/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(len(data["data"]["saves"]), 1)
        
        # Get specific save
        response = requests.get(f"{BASE_URL}/saves/{save_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["data"]["name"], self.test_save["name"])
        
        # Update player
        updated_player = self.test_player.copy()
        updated_player["name"] = "Updated For Save Test"
        response = requests.put(f"{BASE_URL}/players/{player_id}", json=updated_player)
        self.assertEqual(response.status_code, 200)
        
        # Update save
        response = requests.put(f"{BASE_URL}/saves/{save_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Delete player
        response = requests.delete(f"{BASE_URL}/players/{player_id}")
        self.assertEqual(response.status_code, 200)
        self.created_resources["players"].remove(player_id)
        
        # Load save
        response = requests.post(f"{BASE_URL}/saves/{save_id}/load")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Verify player was restored
        response = requests.get(f"{BASE_URL}/players/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        # Find the loaded player
        loaded_player = None
        for player in data["data"]:
            if player["name"] == "Updated For Save Test":
                loaded_player = player
                self.created_resources["players"].append(player["id"])
                break
        
        self.assertIsNotNone(loaded_player, "Player was not loaded from save")
        
        # Create backup
        response = requests.post(f"{BASE_URL}/saves/{save_id}/backup")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        backup_id = data["data"]["backup_id"]
        self.created_resources["saves"].append(backup_id)

if __name__ == "__main__":
    # Wait for server to start
    print("Waiting for server to start...")
    max_retries = 10
    retries = 0
    
    while retries < max_retries:
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("Server is running!")
                break
        except:
            pass
        
        retries += 1
        print(f"Retry {retries}/{max_retries}...")
        time.sleep(2)
    
    if retries == max_retries:
        print("Could not connect to server. Make sure it's running on http://localhost:8000")
        sys.exit(1)
    
    # Run tests
    unittest.main()
