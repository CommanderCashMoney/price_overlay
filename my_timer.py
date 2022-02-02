import time


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    timers = dict()
    def __init__(self, name=None, text="Elapsed time: {:0.4f} seconds"):
        self._start_time = None
        self.text = text
        self.name = name

        if name:
            self.timers.setdefault(name, 0)

    def start(self):
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.name:
            self.timers[self.name] += elapsed_time

        # print(self.text.format(elapsed_time))

    def restart(self):
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        self.stop()
        self.start()

    def elapsed(self, text="Elapsed time: {:0.4f} seconds"):
        if self._start_time:
            elapsed_time = time.perf_counter() - self._start_time
        else:
            elapsed_time = 0
        self.text = text
        return elapsed_time

    def get_total_time(self):
        return self.timers[self.name]
