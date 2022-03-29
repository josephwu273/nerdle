#code borrowed from https://code-maven.com/python-time-left
import datetime

class Timer(object):
    def __init__(self, total, disp=False):
        self.start = datetime.datetime.now()
        self.total = total
        if disp:
            print(f"Process started at {self.start}")
 
    def remains(self, done):
        now  = datetime.datetime.now()
        #print(now-start)  # elapsed time
        left = (self.total - done) * (now - self.start) / done
        sec = int(left.total_seconds())
        if sec < 60:
           return f"{sec} seconds"
        elif sec<3600:
           return f"{int(sec/60)} minutes"
        else:
            return f"{int(sec/3600)} hours; {int((sec%3600)/60)} minutes"