import Pyro5.api
import Process
import time

@Pyro5.api.expose
def iniciar_servidor(gerenciador: 'Process'):
    daemon = Pyro5.api.Daemon(host="localhost", port=9090)  # Cria um daemon Pyro que escuta na porta 9090 no localhost
    uri = daemon.register(gerenciador, "gerenciador.concorrencia")  # Registra o objeto no daemon com um nome específico
    print(f"Servidor disponível. URI: {uri}")  # Imprime a URI do objeto para facilitar o acesso pelo cliente
    daemon.requestLoop()  # Entra no loop de requisições para processar chamadas remotas

if __name__ == "__main__":
    gerenciador = Process.Process(id=1, isCoord=True)  # Cria uma instância do objeto GerenciamentoConcorrencia
    iniciar_servidor(gerenciador)  # Inicia o servidor quando o script é executado
    time.sleep(10)
    gerenciador.derrubar_coordenador()

