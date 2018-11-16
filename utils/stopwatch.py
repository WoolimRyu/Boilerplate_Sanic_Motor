import time


class StopWatch(object):
    def __init__(self):
        self._start = 0
        self._laps = []
        self._stop = 0
    
    def start(self):
        self._start = time.time()
        return self._start

    def stop(self):
        self._stop = time.time()
        return self._stop

    def lap(self):
        lap_time = time.time()
        self._laps.append(lap_time)
        return lap_time
    
    def laps(self):
        return self._laps
    
    def elapsed(self):
        return self._stop - self._start
    