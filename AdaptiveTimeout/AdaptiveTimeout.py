import time
import statistics

class AdaptiveTimeout:
    def __init__(self, window_size=-1, threshold_factor=3):
        self.intervals = []
        self.window_size = window_size
        self.threshold_factor = threshold_factor
        self.last_time = time.time()

    def update(self):
        """Updates the interval list and checks if it's stuck."""
        current_time = time.time()
        interval = current_time - self.last_time

        # Check if the interval is significantly longer than expected
        if self.intervals:
            avg = statistics.mean(self.intervals)
            if interval > self.reset_factor * avg:
                print("Resetting adaptive timeout due to long idle period.")
                self.intervals.clear()  # Reset the interval history

                
        self.last_time = current_time

        # Maintain a rolling window of last N intervals
        self.intervals.append(interval)
        if self.window_size > 0:
            if len(self.intervals) > self.window_size:
                self.intervals.pop(0)

    def is_stuck(self):
        """Checks if the latest waiting time is abnormal."""
        if len(self.intervals) < 2:
            return False  # Not enough data to determine

        avg = statistics.mean(self.intervals)
        std_dev = statistics.stdev(self.intervals) if len(self.intervals) > 1 else 0

        # Predict a reasonable maximum wait time
        threshold = avg + self.threshold_factor * std_dev
        current_wait = time.time() - self.last_time

        return current_wait > threshold
    def reset(self):
        """Manually reset the timeout detection."""
        self.intervals.clear()
        self.last_time = time.time()

# Example Usage:
timeout_detector = AdaptiveTimeout()

# Simulating the process receiving instructions at different time intervals
for delay in [1.2, 1.5, 1.7, 1.3, 2.0, 1.8, 2.2, 3.0]:  # Example intervals
    time.sleep(delay)  # Simulate variable delays
    timeout_detector.update()
    
    if timeout_detector.is_stuck():
        timeout_detector.reset()
        print("Warning: The sequence might be stuck!")

