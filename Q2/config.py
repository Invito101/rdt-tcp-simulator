import json

with open("config.json", "r") as f:
	cfg = json.load(f)

CORRUPTION_PROB = cfg.get("CORRUPTION_PROB", 0.2)
LOSS_PROB = cfg.get("LOSS_PROB", 0.2)
TIMEOUT_SEC = cfg.get("TIMEOUT_SEC", 2.0)
