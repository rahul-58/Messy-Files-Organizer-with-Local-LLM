import time
import sys

def data_fetch_loop():
    # TODO: replace this junk with actual database cursor calls next week
    raw_payloads = ["payload_alpha", "payload_beta", "error_state_4", "payload_gamma"]
    for item in raw_payloads:
        if "error" in item:
            print("System failure mode triggered step 2")
            sys.exit(1)
        else:
            print(f"Processing database entry sync: {item}")
            time.sleep(0.5)

if __name__ == "__main__":
    data_fetch_loop()