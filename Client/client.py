import Pyro5.api

class Cliente:
    def __init__(self, id_cliente):
        self.id_cliente = id_cliente  # Define o ID único do cliente
        self.uri = "PYRO:gerenciador.concorrencia@localhost:9090"  # URI do objeto remoto no servidor
        self.gerenciador = Pyro5.api.Proxy(self.uri)  # Cria um proxy para o objeto remoto

    def acessar_recurso(self):
        resposta = self.gerenciador.acessar_recurso(self.id_cliente)  # Chama o método remoto acessar_recurso
        print(resposta)  # Imprime a resposta recebida do servidor

    def liberar_recurso(self):
        resposta = self.gerenciador.liberar_recurso(self.id_cliente)  # Chama o método remoto liberar_recurso
        print(resposta)  # Imprime a resposta recebida do servidor

    def estado_recurso(self):
        resposta = self.gerenciador.estado_recurso()  # Chama o método remoto estado_recurso
        print(resposta)  # Imprime a resposta recebida do servidor

    def listar_fila_espera(self):
        resposta = self.gerenciador.listar_fila_espera()  # Chama o método remoto listar_fila_espera
        print(resposta)  # Imprime a resposta recebida do servidor

if __name__ == "__main__":
    cliente1 = Cliente(1)  # Cria um cliente com ID "cliente1"
    cliente2 = Cliente(2)  # Cria um cliente com ID "cliente2"
    cliente3 = Cliente(3)
    
    cliente1.acessar_recurso()  # Cliente tenta acessar o recurso
    cliente2.acessar_recurso()  # Cliente tenta acessar o recurso
    cliente3.acessar_recurso()
    cliente1.estado_recurso()  # Cliente verifica o estado do recurso
    cliente1.listar_fila_espera()  # Cliente lista os clientes na fila de espera
    cliente1.liberar_recurso()  # Cliente tenta liberar o recurso    
    cliente2.estado_recurso()  # Cliente verifica o estado do recurso
    cliente2.listar_fila_espera()  # Cliente lista os clientes na fila de espera
    cliente2.liberar_recurso()  # Cliente tenta liberar o recurso
