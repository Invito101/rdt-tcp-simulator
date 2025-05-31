import threading
from packet import Packet
from channel import transmit
from datetime import datetime
from config import TIMEOUT_SEC

class Sender:
	def __init__(self):
		self.seq_num = 0
		self.current_packet = None
		self.timer = None
		self.ack_received = threading.Event()

	def send(self, data, receiver):
		self.current_packet = Packet(self.seq_num, data)
		self.ack_received.clear()
		print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Sending: {self.current_packet}")

		def timeout_handler():
			if not self.ack_received.is_set():
				print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Timeout! Retransmitting...")
				self.send(data, receiver)

		self.timer = threading.Timer(TIMEOUT_SEC, timeout_handler)
		self.timer.start()

		pkt = transmit(self.current_packet)
		if pkt:
			ack = receiver.receive(pkt)
			if ack and not ack.is_corrupted() and ack.seq_num == self.seq_num:
				print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] ACK received: {ack.seq_num}")
				self.timer.cancel()
				self.ack_received.set()
				self.seq_num ^= 1
			else:
				print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] No valid ACK. Waiting for timeout...")

		self.ack_received.wait()

