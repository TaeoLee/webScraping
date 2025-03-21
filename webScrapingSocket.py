import websocket
import json

def on_message(ws, message):
    print("Recieved:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed:", close_status_code, close_msg)

def on_open(ws):
    # Example message payload (obtaoined from browser WebSocket logs)
    init_message = json.jumps({
        
    })