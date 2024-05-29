import Pyro5.api
import threading
import queue


@Pyro5.api.expose
class Coordinator:
    def __init__(self):
        self.lock = threading.Lock()

    def request_acess(self):
        self.lock.acquire()

    def release_acess(self):
        self.lock.release()

def main():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(Coordinator)
    ns.register()



