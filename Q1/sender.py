from datetime import datetime
from packet import Packet
from receiver import Receiver
from channel import transmit

class Sender:
	def __init__(self):
		self.seq_num = 0
		self.current_packet = None

	# Send data to the receiver
	def send(self, data: str, receiver: Receiver) -> None:
		print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Sending data: {data}")
		self.current_packet = Packet(self.seq_num, data)

		while True:
			sent_packet = transmit(self.current_packet)
			ack = receiver.receive(sent_packet)

			if ack and not ack.is_corrupted():
				if ack.seq_num == self.seq_num:
					print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Received valid ACK for seq {ack.seq_num}. Proceeding.")
					self.seq_num ^= 1
					return
				else:
					print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Duplicate ACK received. Retransmitting...")
			else:
				print(f"[SENDER - {datetime.now().strftime("%H:%M %d-%m-%Y")}] Corrupted or invalid ACK. Retransmitting...")
