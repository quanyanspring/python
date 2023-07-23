import time
from datetime import datetime,timedelta
import pprint

def wacth():
    print("Press ENTER to begin, Press Ctrl + C to stop")
    while True:
        try:
            input()  # For ENTER. Use raw_input() if you are running python 2.x instead of input()
            starttime = time.time()
            print("Started")
            while True:
                print("Time Elapsed: ", round(time.time() - starttime, 0), "secs", end="\r")
                time.sleep(1)  # 1 second delay
        except KeyboardInterrupt:
            print("Stopped")
            endtime = time.time()
            print("Total Time:", round(endtime - starttime, 2), "secs")
            break

if __name__ == "__main__":
    wacth()
