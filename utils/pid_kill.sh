#!/bin/bash

# Find the PID of the Python script
pid=$(ps aux | grep "[a]pp.py" | awk '{print $2}')

# Check if the PID is found
if [ -n "$pid" ]; then
    echo "PID found: $pid"
    sudo kill -9 "$pid"
    echo "Process killed."
else
    echo "No matching process found."
fi
