import zlib

class Packet:
	def __init__(self, seq_num, data):
		self.seq_num = seq_num
		self.data = data
		self.checksum = self.compute_checksum()

	def compute_checksum(self):
		return zlib.crc32(f"{self.seq_num}{self.data}".encode())

	def is_corrupted(self):
		return self.checksum != self.compute_checksum()
	
	def __str__(self):
		return f"Packet(seq_num={self.seq_num}, data={self.data}, checksum={self.compute_checksum()})"