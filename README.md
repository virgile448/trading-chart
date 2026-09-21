# Trading Chart

Application web de visualisation de graphiques financiers, construite avec [Lightweight Charts](https://github.com/tradingview/lightweight-charts) (TradingView), avec support d'indicateurs techniques personnalisés en JavaScript.

## Fonctionnalités

- Graphique en chandeliers interactif (zoom, pan, crosshair)
- Indicateur SMA (moyenne mobile simple) personnalisé
- Connexion à des flux de données réels via un proxy local (OANDA v20 API)
- Repli automatique sur des données de démonstration si le flux temps réel n'est pas disponible

## Démo en ligne

👉 [Voir la démo](https://virgile448.github.io/trading-chart/)

## Structure

- `index.html` — page principale (graphique + logique JS)
- `oanda_proxy.py` — proxy Python (Flask) qui relaie les données OANDA sans exposer la clé API au navigateur

## Utilisation avec des données réelles

```bash
pip install flask flask-cors requests
export OANDA_TOKEN="ton_token_ici"
export OANDA_ACCOUNT_ENV="practice"
python oanda_proxy.py
```

Puis ouvre `index.html` dans un navigateur — la page essaie automatiquement de contacter le proxy sur `localhost:8000`, et bascule sur des données de démo si celui-ci n'est pas lancé.

## Technologies

- [Lightweight Charts](https://www.tradingview.com/lightweight-charts/) (Apache 2.0)
- JavaScript vanilla, sans framework
- Proxy backend en Python (Flask)
