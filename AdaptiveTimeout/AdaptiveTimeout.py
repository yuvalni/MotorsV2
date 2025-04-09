import time
import threading
import statistics
import requests

class AdaptiveTimeout:
    def __init__(self, window_size=-1, threshold_factor=6, alert_callback=None, min_timeout=1.0, default_timeout=60*10*2):
        self.intervals = []
        self.window_size = window_size
        self.threshold_factor = threshold_factor
        
        self.last_time = None
        self.timeout_timer = None
        
        self.alert_callback = alert_callback or self.default_alert
        
        self.min_timeout = min_timeout  # Minimum timeout (avoiding zero)
        self.default_timeout = default_timeout  # Timeout when there's no data

    def update(self):
        """Call this when your system successfully makes progress (e.g., finishes a step)."""
        current_time = time.time()
        
        if self.last_time is not None:
            # Calculate interval since last successful step
            interval = current_time - self.last_time
            if interval < 2:
                return True
            self.intervals.append(interval)
            
            # Maintain rolling window
            if self.window_size > 0 and len(self.intervals) > self.window_size:
                self.intervals.pop(0)
            

            print(f"[INFO] Step completed in {interval:.2f} seconds.")
        
        # Mark this time as the last successful update
        self.last_time = current_time

        # Restart the timeout timer
        self.restart_timer()

    def restart_timer(self):
        """Cancel and restart the timeout timer based on predicted thresholds."""
        # Cancel any existing timer
        if self.timeout_timer:
            self.timeout_timer.cancel()
        if len(self.intervals) < 3:  #I don't want to start the timer before buffering a bit
            return True
        # Predict how long we should wait before declaring it stuck
        threshold = self.predict_threshold()
        print(f"[INFO] Restarting timer. Next timeout in {threshold:.2f} seconds.")

        self.timeout_timer = threading.Timer(threshold, self.handle_timeout)
        self.timeout_timer.start()

    def predict_threshold(self):
        """Predict a reasonable maximum wait time."""
        if len(self.intervals) < 3:
            return self.default_timeout  # Not enough data yet

        avg = statistics.mean(self.intervals)
        std_dev = statistics.stdev(self.intervals)

        threshold = avg + self.threshold_factor * std_dev
        return max(threshold, self.min_timeout)

    def handle_timeout(self):
        """Called when timeout expires without an update."""
        print("[ALERT] No update received in predicted time! System might be stuck.")
        if self.alert_callback:
            self.alert_callback()
        self.intervals.clear()
        self.last_time = None

    def default_alert(self):
        """Default alert action (send a message)."""
        print("[DEFAULT ALERT] Sending stuck notification...")


    def reset(self):
        """Manual reset (clears intervals and cancels timers)."""
        #print("[INFO] Manual reset triggered.")
        self.intervals.clear()
        self.last_time = None
        
        if self.timeout_timer:
            self.timeout_timer.cancel()
            self.timeout_timer = None
