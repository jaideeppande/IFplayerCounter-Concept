import websocket
import json

# Replace with your Infinite Flight API key.
API_KEY = "YOUR_API_KEY_HERE"
# The WebSocket endpoint for Infinite Flight Connect API (verify in the documentation).
WS_URL = "wss://connect.infiniteflight.com/ws"

def on_message(ws, message):
    """
    Callback for when a new message is received.
    It processes incoming JSON messages and prints live player counts.
    """
    try:
        data = json.loads(message)
        # Check if the message contains live player count data.
        if data.get("channel") == "live_player_counts":
            print("Live Player Counts:")
            for server in data.get("data", {}).get("servers", []):
                name = server.get("name", "Unknown")
                players = server.get("players", 0)
                print(f"  {name}: {players}")
        else:
            print("Received message:", data)
    except json.JSONDecodeError:
        print("Received non-JSON message:", message)

def on_error(ws, error):
    """
    Callback for when an error occurs.
    """
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    """
    Callback for when the WebSocket connection is closed.
    """
    print("WebSocket closed with code:", close_status_code, "and message:", close_msg)

def on_open(ws):
    """
    Callback for when the WebSocket connection is established.
    Sends authentication and subscription messages.
    """
    print("Connection established. Authenticating...")
    # Authenticate using your API key.
    auth_msg = json.dumps({
        "action": "authenticate",
        "apiKey": API_KEY
    })
    ws.send(auth_msg)

    print("Subscribed to live player counts.")
    # Subscribe to live player count updates.
    sub_msg = json.dumps({
        "action": "subscribe",
        "channel": "live_player_counts"
    })
    ws.send(sub_msg)

if __name__ == "__main__":
    # Enable trace for debugging purposes (optional)
    websocket.enableTrace(True)
    # Create a WebSocketApp with all the callbacks
    ws_app = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    # Run the WebSocket app forever
    ws_app.run_forever()
