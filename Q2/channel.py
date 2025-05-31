import random
import copy
from datetime import datetime
from config import CORRUPTION_PROB, LOSS_PROB
from packet import Packet

def flip_bit(data: str) -> str:
	if not data:
		return data
	index = random.randint(0, len(data) - 1)
	original_char = data[index]
	flipped_char = chr(ord(original_char) ^ 1)
	return data[:index] + flipped_char + data[index + 1:]

def transmit(packet: Packet) -> Packet | None:
	if random.random() < LOSS_PROB:
		print(f"[CHANNEL - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Packet lost.")
		return None

	pkt = copy.deepcopy(packet)
	if random.random() < CORRUPTION_PROB:
		pkt.data = flip_bit(pkt.data)
		print(f"[CHANNEL - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Packet corrupted.")
	else:
		print(f"[CHANNEL - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Packet sent intact.")
	return pkt
