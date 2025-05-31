import json

with open("config.json", "r") as f:
	cfg = json.load(f)

INITIAL_SSTHRESH = cfg.get("INITIAL_SSTHRESH", 16)
TRANSMISSION_ROUNDS = cfg.get("TRANSMISSION_ROUNDS", 100)
MSS = cfg.get("MSS", 1)

LOSS_EVENT_RANDOM = bool(cfg.get("LOSS_EVENT_RANDOM", True))
LOSS_EVENT_PROBABILITY = int(cfg.get("LOSS_EVENT_PROBABILITY", 0))

LOSS_EVENT_INTERVALS = cfg.get("LOSS_EVENT_INTERVALS", [])
LOSS_EVENT_INTERVALS = [int(interval) for interval in LOSS_EVENT_INTERVALS]
