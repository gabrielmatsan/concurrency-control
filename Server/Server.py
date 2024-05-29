import Pyro5.api
import threading


@Pyro5.api.expose
class Coordinator:
    def __init__(self):
        self.lock = threading.Lock()

    def request_access(self):
        self.lock.acquire()
        return True

    def release_access(self):
        self.lock.release()

def main():
    daemon = Pyro5.api.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(Coordinator)
    ns.register("coordenador_one", uri)

    print("Coordenador-pronto")

    daemon.requestLoop()

if __name__ == "__main__":
    main()


