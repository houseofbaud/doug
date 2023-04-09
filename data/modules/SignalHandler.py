import signal

class signalHandler:
	LAST_SIGNAL = 0

	def __init__(self):
		signal.signal(signal.SIGINT, self.signal_handler)
		print("signalHandler_init: successfully initialized signal handler module")

	def signal_handler(self, sig, frame):
		self.LAST_SIGNAL = sig
		if sig == signal.SIGINT:
			print("\n" + str(self.LAST_SIGNAL) + ": ", end="")		
		return

	def get_last_signal(self):
		return self.LAST_SIGNAL

	def reset_signal(self):
		self.LAST_SIGNAL = 0
		return