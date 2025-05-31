from sender import Sender
from receiver import Receiver

def run_simulation():
	sender = Sender()
	receiver = Receiver()

	for msg in ["Hello", "from", "RDT", "2.2", "Protocol"]:
		print("\n---")
		sender.send(msg, receiver)

if __name__ == "__main__":
	run_simulation()
