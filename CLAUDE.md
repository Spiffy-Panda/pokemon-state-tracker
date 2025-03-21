# Pokemon State Tracker Guidelines

## Setup and Commands
- **Install dependencies**: `pip install -r requirements.txt`
- **Run server**: `python -m server.main`
- **Run all tests**: `./run_tests.sh` 
- **Run single test**: `python -m unittest tests.test_api.PokemonPlayerStateTrackerTest.test_player_crud`

## Code Style Guidelines
- **Imports**: Standard libs first, third-party packages next, local imports last
- **Type Hints**: Use throughout (function params/returns, class attributes, collections)
- **Naming**: Classes: PascalCase; Functions/variables: snake_case; Constants: UPPERCASE
- **API Pattern**: Use APIResponse model with success, message, data fields
- **Error Handling**: Raise HTTPException with appropriate status codes and detail messages
- **Indentation**: 4 spaces
- **Line Length**: Keep under 100 characters
- **Documentation**: Docstrings for classes and functions, comments for complex logic
- **Models**: Use Pydantic for data validation; Base models with Create/Update variants

## Project Structure
- **server/**: Main application code
- **server/models/**: Data models and schemas using Pydantic
- **server/api/**: API endpoint implementations
- **server/utils/**: Utility functions
- **tests/**: Test code using Python's unittest framework