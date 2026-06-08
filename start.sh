#!/bin/bash

echo "Starting Chatbot version 2.2 Backend (Port 8000)..."
source venv/bin/activate
uvicorn core:app --port 8000 --reload &
BACKEND_PID=$!

echo "Starting Chatbot version 2.2 Frontend (Port 5173)..."
cd frontend
npm run dev -- --port 5173 &
FRONTEND_PID=$!

echo "========================================"
echo "    Chatbot version 2.2 is running!"
echo " Open http://localhost:5173 in your browser"
echo " Press Ctrl+C to stop both servers"
echo "========================================"

# Cleanup function to kill both processes when the script exits
function cleanup {
    echo -e "\nStopping Chatbot version 2.2 servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap Ctrl+C (SIGINT) to call the cleanup function
trap cleanup SIGINT

# Wait for background processes
wait
