#!/bin/bash

# Start the Pokemon Player State Tracker server
echo "Starting Pokemon Player State Tracker server..."
cd /home/ubuntu/pokemon_state_tracker
source venv/bin/activate
python -m server.main_new &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Run the tests
echo "Running tests..."
mkdir -p tests
python tests/test_api.py

# Shutdown the server
echo "Shutting down server..."
kill $SERVER_PID

echo "Test completed!"
