import Pyro5.api
import time
from threading import Thread
import Process  # Assuming Process class is saved in process.py

# List to keep track of processes for election
processes = []

def iniciar_servidor(gerenciador: 'Process'):
    daemon = Pyro5.api.Daemon(host="localhost", port=9090)  # Create a Pyro daemon listening on port 9090 on localhost
    uri = daemon.register(gerenciador, "gerenciador.concorrencia")  # Register the object with the daemon using a specific name
    print(f"Servidor disponível. URI: {uri}")  # Print the URI of the object to facilitate client access
    
    # Function to stop the daemon after 5 seconds
    def stop_daemon_after_delay():
        time.sleep(5)  # Wait for 5 seconds
        daemon.shutdown()  # Stop the daemon
        print(f"Coordinator {gerenciador.id} is shutting down. Initiating election.")
        
        # Simulate the election process
        for process in processes:
            if process.id != gerenciador.id:
                process.iniciar_eleicao(processes)
                break  # Only one process needs to initiate the election

    # Start the stop function in a separate thread
    stop_thread = Thread(target=stop_daemon_after_delay)
    stop_thread.start()

    daemon.requestLoop()  # Enter the request loop to process remote calls

if __name__ == "__main__":
    # Create an instance of the Process as the initial coordinator
    gerenciador = Process.Process(id=1, isCoord=True)
    processes.append(gerenciador)  # Add to processes list

    # Create additional processes
    process2 = Process.Process(id=2)
    process3 = Process.Process(id=3)
    processes.append(process2)
    processes.append(process3)

    # Start the server
    server_thread = Thread(target=iniciar_servidor, args=(gerenciador,))
    server_thread.daemon = True
    server_thread.start()

    # Simulate client processes accessing resources
    time.sleep(1)  # Ensure the server is started

    # Keep the main thread alive to allow background threads to run
    while True:
        time.sleep(1)
