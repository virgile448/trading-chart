"""
Proxy local entre ta page web (Lightweight Charts) et l'API OANDA v20.
La clé API reste côté serveur, jamais exposée au navigateur.

Installation :
    pip install flask flask-cors requests

Configuration :
    Définis tes variables d'environnement avant de lancer, ex (Linux/Kali) :
        export OANDA_TOKEN="ton_token_ici"
        export OANDA_ACCOUNT_ENV="practice"   # ou "live"

Lancement :
    python oanda_proxy.py
    -> Le proxy écoute sur http://localhost:8000

Utilisation depuis le navigateur :
    GET http://localhost:8000/candles?instrument=EUR_USD&granularity=M5&count=200
"""

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # autorise la page HTML (fichier local ou autre port) à appeler ce proxy

OANDA_TOKEN = os.environ.get("OANDA_TOKEN", "")
OANDA_ENV = os.environ.get("OANDA_ACCOUNT_ENV", "practice")  # "practice" ou "live"

HOSTS = {
    "practice": "https://api-fxpractice.oanda.com",
    "live": "https://api-fxtrade.oanda.com",
}


@app.route("/candles")
def candles():
    if not OANDA_TOKEN:
        return jsonify({"error": "OANDA_TOKEN non défini côté serveur"}), 500

    instrument = request.args.get("instrument", "EUR_USD")
    granularity = request.args.get("granularity", "M5")
    count = request.args.get("count", "200")

    url = f"{HOSTS[OANDA_ENV]}/v3/instruments/{instrument}/candles"
    headers = {"Authorization": f"Bearer {OANDA_TOKEN}"}
    params = {"granularity": granularity, "count": count, "price": "M"}  # M = midpoint

    r = requests.get(url, headers=headers, params=params, timeout=10)
    if r.status_code != 200:
        return jsonify({"error": "Erreur OANDA", "detail": r.text}), r.status_code

    raw = r.json().get("candles", [])

    # Reformate pour Lightweight Charts : { time, open, high, low, close }
    out = []
    for c in raw:
        if not c.get("complete", True):
            continue
        t = c["time"][:19] + "Z"  # ISO -> on garde jusqu'à la seconde
        import datetime
        unix_time = int(datetime.datetime.fromisoformat(t.replace("Z", "+00:00")).timestamp())
        out.append({
            "time": unix_time,
            "open": float(c["mid"]["o"]),
            "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]),
            "close": float(c["mid"]["c"]),
        })

    return jsonify(out)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
