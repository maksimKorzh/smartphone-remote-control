#!/bin/bash

# Working directory
cd /home/cmk/smartphone-remote-control/src/

# Start HTTP server in the background
nohup python3 app.py > http.log 2>&1 &

# Start UDP server in the background
nohup python3 udp.py > udp.log 2>&1 &

# Optionally print their PIDs
echo "HTTP server started with PID $!"
HTTP_PID=$!

sleep 1  # short pause to avoid PID overlap

echo "UDP server started with PID $!"
UDP_PID=$!
