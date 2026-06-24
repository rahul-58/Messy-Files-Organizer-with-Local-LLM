import time
import subprocess
import sys

print("Running organize.py every 5 minutes...")
print("Press Ctrl+C to stop the automation.")

try:
    while True:

        subprocess.run([sys.executable, "organize.py"])
        
        # Sleeps for 5 minutes (300 seconds)
        time.sleep(300)

except KeyboardInterrupt:
    print("\n Automation stopped.")