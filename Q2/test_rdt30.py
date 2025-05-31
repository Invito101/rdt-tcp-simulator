from sender import Sender
from receiver import Receiver
import time

def run():
	sender = Sender()
	receiver = Receiver()

	for msg in ["Hello", "from", "RDT", "3.0", "Protocol"]:
		print("\n---")
		sender.send(msg, receiver)
		time.sleep(0.5)

if __name__ == "__main__":
	run()
