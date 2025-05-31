from packet import Packet
from datetime import datetime

class Receiver:
	def __init__(self):
		self.expected_seq = 0
		self.last_ack = None

	def receive(self, packet):
		print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Got: {packet}")
		if not packet or packet.is_corrupted():
			print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Corrupted or lost packet. Sending duplicate ACK.")
			return self.last_ack

		if packet.seq_num == self.expected_seq:
			print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Delivering data: {packet.data}")
			ack = Packet(packet.seq_num, "ACK")
			self.last_ack = ack
			self.expected_seq ^= 1
			return ack
		else:
			print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Duplicate packet. Sending last ACK.")
			return self.last_ack
