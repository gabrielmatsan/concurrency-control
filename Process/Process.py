import Pyro5.api

@Pyro5.api.expose
class Process:
    def __init__(self, id, uri="PYRO:gerenciador.concorrencia@localhost:9090"):
        self.id = id # Define o ID único do processo
        self.uri = uri   # URI do objeto remoto no servidor
        self.gerenciador = Pyro5.api.Proxy(self.uri)  # Cria um proxy para o objeto remoto
        self.recurso = None  # Inicializa o recurso como None, indicando que não está alocado
        self.fila_espera = []  # Lista para gerenciar a fila de espera

    def acessar_recurso(self):
        resposta = self.gerenciador.coordenador_acessar_recurso(self.id)  # Chama o método remoto acessar_recurso
        print(resposta)  # Imprime a resposta recebida do servidor

    def liberar_recurso(self):
        resposta = self.gerenciador.coordenador_liberar_recurso(self.id)  # Chama o método remoto liberar_recurso
        print(resposta)  # Imprime a resposta recebida do servidor

    def estado_recurso(self):
        resposta = self.gerenciador.coordenador_estado_recurso()  # Chama o método remoto estado_recurso
        print(resposta)  # Imprime a resposta recebida do servidor

    def listar_fila_espera(self):
        resposta = self.gerenciador.coordenador_listar_fila_espera()  # Chama o método remoto listar_fila_espera
        print(resposta)  # Imprime a resposta recebida do servidor

    def coordenador_acessar_recurso(self, id):
        if self.recurso is None:  # Verifica se o recurso não está alocado
            self.recurso = id  # Aloca o recurso para o cliente que fez a requisição
            return f"Recurso alocado para o cliente {id}"
        else:
            # Adiciona o cliente à fila de espera
            self.fila_espera.append(id)
            return f"Recurso já alocado para o cliente {self.recurso}. Cliente {id} adicionado à fila de espera"

    def coordenador_liberar_recurso(self, id):
        if self.recurso == id:  # Verifica se o cliente que fez a requisição é o dono do recurso
            self.recurso = None  # Libera o recurso
            if self.fila_espera:
                # Aloca o recurso para o próximo cliente na fila de espera
                proximo_cliente = self.fila_espera.pop(0)
                self.recurso = proximo_cliente
                return f"Recurso liberado pelo cliente {id} e alocado para o cliente {proximo_cliente}"
            return f"Recurso liberado pelo cliente {id}. Nenhum cliente na fila de espera"
        else:
            return f"Cliente {id} não possui o recurso"  # Informa que o cliente não possui o recurso para liberá-lo

    def coordenador_estado_recurso(self):
        if self.recurso is None:
            return "O recurso está disponível"
        else:
            return f"O recurso está alocado para o cliente {self.recurso}"

    def coordenador_listar_fila_espera(self):
        if self.fila_espera:
            return f"Clientes na fila de espera: {', '.join(map(str, self.fila_espera))}"
        else:
            return "Não há clientes na fila de espera"