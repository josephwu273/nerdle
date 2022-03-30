#code borrowed from https://code-maven.com/python-time-left
import datetime

class Timer(object):
    def __init__(self, total, disp=False):
        self.start = datetime.datetime.now()
        self.total = total
        if disp:
            print(f" Process started at {self.start}")

    def finish(self, done):
        now = datetime.datetime.now()
        left = (self.total - done) * (now - self.start) / done
        finish = now+left
        return f"{finish.strftime('%H:%M')}"
 
    
    def remains(self, done):
        now  = datetime.datetime.now()
        #print(now-start)  # elapsed time
        left = (self.total - done) * (now - self.start) / done
        sec = int(left.total_seconds())
        if sec < 60:
           return f"{sec}s"
        elif sec<3600:
           return f"{int(sec/60)}min"
        else:
            h = sec//3600
            m = (sec%3600)//60
            return f"{h} hours, {m} minutes"