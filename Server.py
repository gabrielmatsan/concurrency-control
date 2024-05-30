import Pyro5.api
from process import Process as p

@Pyro5.api.expose
def iniciar_servidor():
    gerenciador = p()  # Cria uma instância do objeto GerenciamentoConcorrencia
    daemon = Pyro5.api.Daemon(host="localhost", port=9090)  # Cria um daemon Pyro que escuta na porta 9090 no localhost
    uri = daemon.register(gerenciador, "gerenciador.concorrencia")  # Registra o objeto no daemon com um nome específico
    print(f"Servidor disponível. URI: {uri}")  # Imprime a URI do objeto para facilitar o acesso pelo cliente
    daemon.requestLoop()  # Entra no loop de requisições para processar chamadas remotas

if __name__ == "__main__":
    iniciar_servidor()  # Inicia o servidor quando o script é executado
