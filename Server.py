import Pyro5.api
import time
from threading import Thread
import Process 
from Process import processes

def iniciar_servidor(gerenciador: 'Process'):
    daemon = Pyro5.api.Daemon(host="localhost", port=9090)
    uri = daemon.register(gerenciador, "gerenciador.concorrencia")
    print(f"Servidor disponível. URI: {uri}")

    time.sleep(10)

    def stop_daemon_after_delay():
        time.sleep(10)  # Wait for 10 seconds
        daemon.shutdown()  # Stop the daemon
        print(f"Coordinator {gerenciador.id} is shutting down. Initiating election.")
        for process in processes:
            if process.id != gerenciador.id:
                process.iniciar_eleicao()
                break

    stop_thread = Thread(target=stop_daemon_after_delay)
    stop_thread.start()

    daemon.requestLoop()

if __name__ == "__main__":
    gerenciador = Process.Process(id=1, isCoord=True)
    processes.append(gerenciador)
    process2 = Process.Process(id=2)
    process3 = Process.Process(id=3)
    processes.append(process2)
    processes.append(process3)

    server_thread = Thread(target=iniciar_servidor, args=(gerenciador,))
    server_thread.daemon = True
    server_thread.start()

    while True:
        time.sleep(5)
