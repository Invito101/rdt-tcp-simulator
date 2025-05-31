import random
import copy
from datetime import datetime
from packet import Packet
from config import CORRUPTION_PROB

# Flip bits in a string
def flip_bit(data: str) -> str:
	if not data:
		return data
	index = random.randint(0, len(data) - 1)
	original_char = data[index]
	flipped_char = chr(ord(original_char) ^ 1)
	return data[:index] + flipped_char + data[index + 1:]

# Simulate a channel that may introduce bit errors
def transmit(packet: Packet) -> Packet:
	packet_copy = copy.deepcopy(packet)
	if random.random() < CORRUPTION_PROB:
		packet_copy.data = flip_bit(packet_copy.data)
		print(f"[CHANNEL - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Bit error introduced!")
	else:
		print(f"[CHANNEL - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Packet transmitted without error.")
	return packet_copy
