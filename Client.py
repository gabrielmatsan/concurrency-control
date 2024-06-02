import Pyro5.api
import time

def get_process_proxy():
    uri = "PYRO:gerenciador.concorrencia@localhost:9090"
    return Pyro5.api.Proxy(uri)

def simulate_client_processes():
    process_proxy = get_process_proxy()

    try:
        process_proxy.acessar_recurso(2)  # Client with ID 2 tries to access the resource
    except Exception as e:
        print(f"Client 2 failed to access resource: {e}")

    try:
        process_proxy.acessar_recurso(3)  # Client with ID 3 tries to access the resource
    except Exception as e:
        print(f"Client 3 failed to access resource: {e}")

    time.sleep(1)  # Simulate some delay before the next operation

    try:
        process_proxy.liberar_recurso(2)  # Client with ID 2 releases the resource
    except Exception as e:
        print(f"Client 2 failed to release resource: {e}")

    try:
        process_proxy.acessar_recurso(4)  # Client with ID 4 tries to access the resource
    except Exception as e:
        print(f"Client 3 failed to access resource: {e}")

    try:
        process_proxy.liberar_recurso(4)  # Client with ID 3 tries to access the resource
    except Exception as e:
        print(f"Client 3 failed to access resource: {e}")


if __name__ == "__main__":
    time.sleep(2)  # Ensure the server is started before the client tries to connect
    simulate_client_processes()
