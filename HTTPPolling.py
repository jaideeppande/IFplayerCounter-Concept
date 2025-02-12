import time
import requests

# Replace with the correct API endpoint that returns live player counts in JSON.
API_ENDPOINT = "https://api.infiniteflight.com/live_player_counts"

def fetch_player_counts():
    """
    Sends an HTTP GET request to retrieve live player count data.
    """
    response = requests.get(API_ENDPOINT)
    response.raise_for_status()  # Raises an exception for HTTP errors.
    return response.json()  # Assumes the API returns JSON.

def main():
    while True:
        try:
            data = fetch_player_counts()
            print("Live Player Counts:")
            # Assume the JSON structure is {"servers": [{"name": "Server1", "players": 15}, ...]}
            for server in data.get("servers", []):
                name = server.get("name", "Unknown")
                players = server.get("players", 0)
                print(f"  {name}: {players}")
        except Exception as e:
            print("Error fetching data:", e)
        # Wait before polling again
        time.sleep(5)

if __name__ == "__main__":
    main()
