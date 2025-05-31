from config import INITIAL_SSTHRESH, TRANSMISSION_ROUNDS, MSS, LOSS_EVENT_INTERVALS, LOSS_EVENT_RANDOM, LOSS_EVENT_PROBABILITY
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random

class TCPTahoeSimulator:
	def __init__(self, mss=1, init_ssthresh=16, total_rtts=100, loss_events=None):
		self.mss = mss
		self.ssthresh = init_ssthresh
		self.total_rtts = total_rtts
		self.loss_events = set(loss_events if loss_events else [])
		
		self.cwnd = mss
		self.log = []

	def simulate(self):
		for t in range(self.total_rtts):
			self.log.append((t, self.cwnd, self.ssthresh))
			
			if t in self.loss_events:
				print(f"Loss detected at RTT {t}: cwnd={self.cwnd} -> 1, ssthresh={max(self.cwnd // 2, 1)}")
				self.ssthresh = max(self.cwnd // 2, 1)
				self.cwnd = self.mss
				continue

			if self.cwnd < self.ssthresh:
				if(2 * self.cwnd > self.ssthresh):
					self.cwnd = self.ssthresh
				else:
					self.cwnd *= 2
			else:
				self.cwnd += self.mss

	def plot(self):
		rtts, cwnds, ssthreshes = zip(*self.log)
		plt.figure(figsize=(10, 6))
		plt.plot(rtts, cwnds, label="cwnd", marker='o')
		plt.plot(rtts, ssthreshes, label="ssthresh", linestyle='--')
		plt.xlabel("RTT")
		plt.ylabel("Window Size (in MSS)")
		plt.title("TCP Tahoe Congestion Control Mechanism")
		plt.legend()
		plt.grid(True)
		plt.savefig("tahoe_plot.png")

	def csv(self):
		with open("tahoe_log.csv", "w") as f:
			f.write("RTT,cwnd,ssthresh\n")
			for t, cwnd, ssthresh in self.log:
				f.write(f"{t+1},{cwnd},{ssthresh}\n")
		print("Log saved to tahoe_log.csv")

if __name__ == "__main__":
	print("Running TCP Tahoe Simulation...")
	print("Initial ssthresh:", INITIAL_SSTHRESH)
	print("Transmission rounds:", TRANSMISSION_ROUNDS)
	print("MSS:", MSS)

	if(LOSS_EVENT_RANDOM == True or LOSS_EVENT_INTERVALS == []):
		print("No loss events detected, simulation will be run with random loss events with setings:")
		if(LOSS_EVENT_PROBABILITY == 0):
			print("Loss event probability is set to 0, defaulting to 0.1")
			LOSS_EVENT_PROBABILITY = 0.1

		print("Loss event probability:", LOSS_EVENT_PROBABILITY)

		for i in range(TRANSMISSION_ROUNDS):
			if LOSS_EVENT_PROBABILITY > 0 and random.random() <= LOSS_EVENT_PROBABILITY:
				LOSS_EVENT_INTERVALS.append(i+1)

		print("Loss events detected at intervals:", LOSS_EVENT_INTERVALS)
	else:
		print("Loss events detected at intervals:", LOSS_EVENT_INTERVALS)

	simulator = TCPTahoeSimulator(
		mss=MSS,
		init_ssthresh=INITIAL_SSTHRESH,
		total_rtts=TRANSMISSION_ROUNDS,
		loss_events=LOSS_EVENT_INTERVALS
	)
	simulator.simulate()
	simulator.plot()
	simulator.csv()
