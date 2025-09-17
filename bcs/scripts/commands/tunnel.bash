#!/usr/bin/env bash

# File: tunnel.bash

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root/bcs/" || exit 1

PID_FILE=".ngrok_pid"
ADDR_FILE=".ngrok_addr"

function start_tunnel() {
  echo "🚀 Starting ngrok tunnel on port 8000..."
  # Run ngrok in background, save its PID
  ngrok http 8000 >/dev/null 2>&1 &
  NGROK_PID=$!
  echo $NGROK_PID >$PID_FILE

  # Wait a bit for ngrok to initialize
  sleep 2

  # Fetch the public URL from ngrok API
  ADDR=$(curl -s http://127.0.0.1:4040/api/tunnels |
    grep -oE "https://[a-z0-9]+\.ngrok-free\.app" | head -n 1)

  if [ -n "$ADDR" ]; then
    echo "🌍 Tunnel available at: $ADDR"
    echo "$ADDR" >$ADDR_FILE
  else
    echo "❌ Failed to retrieve ngrok address."
  fi
}

function end_tunnel() {
  if [ -f $PID_FILE ]; then
    PID=$(cat $PID_FILE)
    echo "🛑 Stopping ngrok tunnel (PID: $PID)..."
    kill "$PID"
    rm -f $PID_FILE $ADDR_FILE
  else
    echo "⚠️ No tunnel is currently running."
  fi
}

case "$1" in
--end)
  end_tunnel
  ;;
*)
  start_tunnel
  ;;
esac
