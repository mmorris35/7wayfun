#!/bin/bash
# Launch the 7-Way Trailer Tester Interactive Simulator

# Change to the project directory
cd "$(dirname "$0")"

echo "=========================================="
echo "  7-Way Trailer Tester Simulator"
echo "=========================================="
echo ""
echo "Starting simulator..."
echo ""

# Run the simulator
python3 simulator/run_simulator.py

# If it exits, show a message
echo ""
echo "Simulator exited."
echo ""
