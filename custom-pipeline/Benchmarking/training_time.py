import time
class BenchmarkTime:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        print(f"Training took: {time.strftime('%H:%M:%S', time.gmtime(self.interval))}")