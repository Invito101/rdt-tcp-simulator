from config import INITIAL_SSTHRESH, TRANSMISSION_ROUNDS, MSS, LOSS_EVENT_INTERVALS, LOSS_EVENT_RANDOM, LOSS_EVENT_PROBABILITY
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random

class TCPRenoSimulator:
	def __init__(self, mss=1, init_ssthresh=16, total_rtts=100, loss_events=None):
		self.mss = mss
		self.ssthresh = init_ssthresh
		self.total_rtts = total_rtts
		self.loss_events = set(loss_events if loss_events else [])
		
		self.cwnd = mss
		self.log = []
		self.in_fast_recovery = False
		self.recover = None

	def simulate(self):
		for t in range(self.total_rtts):
			self.log.append((t, self.cwnd, self.ssthresh))

			if t in self.loss_events:
				print(f"Triple duplicate ACK at RTT {t}: entering fast recovery")
				self.ssthresh = max(self.cwnd // 2, 1)
				self.cwnd = self.ssthresh + 3 * self.mss
				self.in_fast_recovery = True
				self.recover = self.cwnd
				continue

			if self.in_fast_recovery:
				self.cwnd += self.mss
				if self.cwnd >= self.recover + self.mss:
					print(f"Exiting fast recovery at RTT {t}")
					self.cwnd = self.ssthresh
					self.in_fast_recovery = False
				continue

			if self.cwnd < self.ssthresh:
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
		plt.title("TCP Reno Congestion Control Mechanism")
		plt.legend()
		plt.grid(True)
		plt.savefig("reno_plot.png")

	def csv(self):
		with open("reno_log.csv", "w") as f:
			f.write("RTT,cwnd,ssthresh\n")
			for t, cwnd, ssthresh in self.log:
				f.write(f"{t+1},{cwnd},{ssthresh}\n")
		print("Log saved to reno_log.csv")


if __name__ == "__main__":
	print("Running TCP Reno Simulation...")
	print("Initial ssthresh:", INITIAL_SSTHRESH)
	print("Transmission rounds:", TRANSMISSION_ROUNDS)
	print("MSS:", MSS)

	if LOSS_EVENT_RANDOM or not LOSS_EVENT_INTERVALS:
		print("No loss events provided. Generating random loss events.")
		if LOSS_EVENT_PROBABILITY == 0:
			print("Loss probability set to 0, defaulting to 0.1")
			LOSS_EVENT_PROBABILITY = 0.1
		for i in range(TRANSMISSION_ROUNDS):
			if random.random() <= LOSS_EVENT_PROBABILITY:
				LOSS_EVENT_INTERVALS.append(i + 1)
		print("Loss events at intervals:", LOSS_EVENT_INTERVALS)
	else:
		print("Loss events at intervals:", LOSS_EVENT_INTERVALS)

	simulator = TCPRenoSimulator(
		mss=MSS,
		init_ssthresh=INITIAL_SSTHRESH,
		total_rtts=TRANSMISSION_ROUNDS,
		loss_events=LOSS_EVENT_INTERVALS
	)
	simulator.simulate()
	simulator.plot()
	simulator.csv()
