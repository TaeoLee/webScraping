import websocket
import json
import re

subscription_payload = {
    "_event": "bulk-subscribe",
    "tzID": 8,
    "message": "isOpenExch-110:%%pid-43433:%%isOpenExch-60:%%pid-43356:%%pid-43430:%%pid-979183:%%pid-43436:%%pid-43399:%%pid-43544:%%pid-50596:%%pid-43460:%%pid-43542:%%pid-1131302:%%pid-43531:%%pid-43493:%%pid-1010642:%%pid-43472:%%pid-37426:%%pid-8987:%%isOpenExch-1004:%%pid-1175153:%%isOpenExch-152:%%pid-1175151:%%pid-172:%%isOpenExch-4:%%pid-178:%%isOpenExch-20:%%pid-8827:%%pid-8830:%%pid-8836:%%pid-8833:%%pid-8849:%%pid-8862:%%pid-8831:%%pid-8918:%%pid-6408:%%isOpenExch-2:%%pid-941155:%%isOpenExch-1:%%pid-13994:%%pid-254:%%pid-243:%%pid-271:%%pid-7888:%%pid-6369:%%pid-284:%%isOpenExch-3:%%pid-8177:%%pid-350:%%pid-166:%%pid-169:%%pid-20:%%pid-167:%%isOpenExch-9:%%pid-27:%%pid-8917:%%pid-1:%%isOpenExch-1002:%%pid-3:%%pid-650:%%pid-159:%%pid-5:%%pid-9:%%pid-2186:%%pid-1165605:%%pid-1165612:%%pid-1200530:%%pid-1204969:%%pid-953473:%%pid-1061653:%%pid-525:%%pid-14175:%%pid-9429:%%pid-2:%%pid-2055:%%pidExt-1175153:%%cmt-18-5-8839:%%pid-1172292:%%pid-1175355:%%pid-17499:%%pid-992966:%%pid-252:%%pid-25328:%%pid-275:%%pid-7997:%%pid-8358:%%pid-43538:%%isOpenExch-0:%%pid-43600:%%pid-43738:%%pid-43779:%%pid-43796:%%pid-43859:%%pid-44084:%%pid-44106:%%pid-979066:%%pid-43365:%%pid-43406:%%pid-43422:%%pid-43437:%%pid-43495:%%pid-43504:%%pid-43507:"
}

def extract_price(message, target_pid="1175153"):
    sockjs_pattern = r'^a\["(.*)"\]$'
    sockjs_match = re.match(sockjs_pattern, message)

    if sockjs_match:
        inner_message = sockjs_match.group(1).replace('\\"', '"')
        pid_pattern = rf'"message":"pid-{target_pid}::({{.*}})"'
        json_match = re.search(pid_pattern, inner_message)

        if json_match:
            json_str = json_match.group(1).replace('\\"', '"')
            data = json.loads(json_str)
            return data.get('last_numeric')
    return None

def on_message(ws, message):
    if message == "o":
        print("Connected (handshake complete). Sending subscription...")
        subscribe(ws)
        return

    price = extract_price(message, "1175153")
    if price:
        print(f"Real-time price for pid-1175153: {price}")

def subscribe(ws):
    # Send the exact subscription message your browser uses
    payload = '["' + json.dumps(subscription_payload) + '"]'
    ws.send(payload)
    print(f"Subscription sent! {payload}")

def on_open(ws):
    print("WebSocket opened, waiting for handshake...")

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed:", close_status_code, close_msg)

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws_url = "wss://streaming.forexpros.com/echo/250/tmg1xoiv/websocket"

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    ws.run_forever()
