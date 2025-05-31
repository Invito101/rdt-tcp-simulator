import zlib

# This class represents a packet
class Packet:
	def __init__(self, seq_num, data):
		self.seq_num = seq_num
		self.data = data
		self.checksum = self.compute_checksum()

	# Compute the checksum using zlib's crc32
	def compute_checksum(self):
		content = f"{self.seq_num}{self.data}".encode()
		return zlib.crc32(content)

	def is_corrupted(self):
		return self.checksum != self.compute_checksum()
	
	def __str__(self):
		return f"Packet(seq_num={self.seq_num}, data={self.data}, checksum={self.compute_checksum()})"