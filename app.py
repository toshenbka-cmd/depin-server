from flask import Flask, request, jsonify
import time

app = Flask(__name__)
nodes = {}

@app.route('/')
def home():
    current_time = time.time()
    active_nodes = {k: v for k, v in nodes.items() if current_time - v['last_seen'] < 60}
    total_power = sum(node['power'] for node in active_nodes.values())
    return f"""
    <html>
    <head><title>DePIN Monitor</title><meta http-equiv="refresh" content="5"></head>
    <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background: #1a1a1a; color: white;">
        <h1>Моя DePIN Сеть</h1>
        <div style="font-size: 60px; color: #00ff00; margin: 20px 0;"><strong>{total_power:.2f} GFLOPS</strong></div>
        <p style="color: #00ff00;">● СЕТЬ АКТИВНА</p>
        <p>Активных устройств: {len(active_nodes)}</p>
        <p style="color: #666;">Обновлено: {time.strftime('%H:%M:%S')}</p>
    </body></html>
    """

@app.route('/report', methods=['POST'])
def report():
    data = request.get_json(force=True)
    nodes[data.get("node_id", "unknown")] = {"power": data.get("power", 0), "last_seen": time.time()}
    return jsonify({"status": "ok"})
