import Pyro5.api

@Pyro5.api.expose
class GerenciamentoConcorrencia:
    def __init__(self):
        self.recurso = None  # Inicializa o recurso como None, indicando que não está alocado
        self.fila_espera = []  # Lista para gerenciar a fila de espera

    def acessar_recurso(self, cliente_id):
        if self.recurso is None:  # Verifica se o recurso não está alocado
            self.recurso = cliente_id  # Aloca o recurso para o cliente que fez a requisição
            return f"Recurso alocado para o cliente {cliente_id}"
        else:
            # Adiciona o cliente à fila de espera
            self.fila_espera.append(cliente_id)
            return f"Recurso já alocado para o cliente {self.recurso}. Cliente {cliente_id} adicionado à fila de espera"

    def liberar_recurso(self, cliente_id):
        if self.recurso == cliente_id:  # Verifica se o cliente que fez a requisição é o dono do recurso
            self.recurso = None  # Libera o recurso
            if self.fila_espera:
                # Aloca o recurso para o próximo cliente na fila de espera
                proximo_cliente = self.fila_espera.pop(0)
                self.recurso = proximo_cliente
                return f"Recurso liberado pelo cliente {cliente_id} e alocado para o cliente {proximo_cliente}"
            return f"Recurso liberado pelo cliente {cliente_id}. Nenhum cliente na fila de espera"
        else:
            return f"Cliente {cliente_id} não possui o recurso"  # Informa que o cliente não possui o recurso para liberá-lo

    def estado_recurso(self):
        if self.recurso is None:
            return "O recurso está disponível"
        else:
            return f"O recurso está alocado para o cliente {self.recurso}"

    def listar_fila_espera(self):
        if self.fila_espera:
            return f"Clientes na fila de espera: {', '.join(self.fila_espera)}"
        else:
            return "Não há clientes na fila de espera"

def iniciar_servidor():
    gerenciador = GerenciamentoConcorrencia()  # Cria uma instância do objeto GerenciamentoConcorrencia
    daemon = Pyro5.api.Daemon(host="localhost", port=9090)  # Cria um daemon Pyro que escuta na porta 9090 no localhost
    uri = daemon.register(gerenciador, "gerenciador.concorrencia")  # Registra o objeto no daemon com um nome específico
    print(f"Servidor disponível. URI: {uri}")  # Imprime a URI do objeto para facilitar o acesso pelo cliente
    daemon.requestLoop()  # Entra no loop de requisições para processar chamadas remotas

if __name__ == "__main__":
    iniciar_servidor()  # Inicia o servidor quando o script é executado
