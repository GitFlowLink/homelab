from flask import Flask, jsonify, request
from flask_cors import CORS
import json, os
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)
DATA_FILE = '/data/stats.json'

def load():
    if not os.path.exists(DATA_FILE):
        return {"stats": {}, "session": None, "history": []}
    try:
        with open(DATA_FILE) as f:
            d = json.load(f)
            if "history" not in d: d["history"] = []
            return d
    except:
        return {"stats": {}, "session": None, "history": []}

def save(d):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

@app.route('/health')
def health():
    return jsonify({"ok": True})

@app.route('/stats')
def get_stats():
    return jsonify(load())

@app.route('/stats/record', methods=['POST'])
def record():
    b = request.json
    d = load()
    s = d.setdefault('stats', {})
    key = f"{b.get('cat')}||{b.get('subtopic','')}"
    if key not in s:
        s[key] = {"cat": b.get('cat'), "subtopic": b.get('subtopic',''), "correct": 0, "total": 0}
    s[key]['total'] += 1
    if b.get('correct'): s[key]['correct'] += 1
    save(d)
    return jsonify({"ok": True})

@app.route('/session', methods=['GET'])
def get_session():
    return jsonify(load().get('session') or {})

@app.route('/session', methods=['POST'])
def save_session():
    d = load()
    d['session'] = request.json
    save(d)
    return jsonify({"ok": True})

@app.route('/session', methods=['DELETE'])
def clear_session():
    d = load()
    d['session'] = None
    save(d)
    return jsonify({"ok": True})

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(load().get('history', []))

@app.route('/history/add', methods=['POST'])
def add_history():
    b = request.json
    d = load()
    h = d.setdefault('history', [])
    h.append({
        "date": datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        "time": datetime.now(timezone.utc).strftime('%H:%M'),
        "score": b.get('score', 0),
        "total": b.get('total', 0),
        "pct": b.get('pct', 0)
    })
    # keep last 100 entries
    d['history'] = h[-100:]
    save(d)
    return jsonify({"ok": True})

@app.route('/stats/reset', methods=['POST'])
def reset():
    d = load()
    d['stats'] = {}
    d['session'] = None
    save(d)
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
