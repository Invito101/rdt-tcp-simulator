import json

with open("config.json", "r") as f:
	cfg = json.load(f)

CORRUPTION_PROB = cfg.get("CORRUPTION_PROB", 0.2)