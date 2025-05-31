from datetime import datetime
from packet import Packet

class Receiver:
	def __init__(self):
		self.expected_seq = 0
		self.last_ack = None

	# Receive a packet and process it
	def receive(self, packet: Packet) -> Packet:
		print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Received: {packet}")
		if packet.is_corrupted():
			print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Corrupted packet! Sending duplicate ACK.")
			return self.last_ack

		if packet.seq_num == self.expected_seq:
			print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] In-order packet. Delivering: {packet.data}")
			ack = Packet(packet.seq_num, "ACK")
			self.last_ack = ack
			self.expected_seq ^= 1
			return ack
		else:
			print(f"[RECEIVER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Out-of-order (duplicate) packet. Sending last ACK.")
			return self.last_ack
