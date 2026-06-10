#!/bin/bash
cd /home/zain/Documents/vioce.ai

# Purana port file delete karo
rm -f /tmp/jarvis_port.txt

# Server background mein start karo
python3 server.py &
SERVER_PID=$!

# Port file ready hone tak wait karo
for i in {1..30}; do
    if [ -f /tmp/jarvis_port.txt ]; then
        break
    fi
    sleep 0.5
done

PORT=$(cat /tmp/jarvis_port.txt 2>/dev/null || echo "5000")
echo "Jarvis running on port $PORT"

# Browser mein frontend kholo
xdg-open http://127.0.0.1:$PORT

# Server band hone tak ruko
wait $SERVER_PID
