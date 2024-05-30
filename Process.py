import Pyro5.api
from typing import List


@Pyro5.api.expose
class Process:
    def __init__(self, id, uri="PYRO:gerenciador.concorrencia@localhost:9090", isCoord=False):
        self.id = id  # Define o ID único do processo
        self.uri = uri  # URI do objeto remoto no servidor
        self.gerenciador = Pyro5.api.Proxy(self.uri)  # Cria um proxy para o objeto remoto
        self.recurso = None  # Inicializa o recurso como None, indicando que não está alocado
        self.fila_espera = []  # Lista para gerenciar a fila de espera
        self.isCoord = isCoord

    def acessar_recurso(self):
        try:
            resposta = self.gerenciador.coordenador_acessar_recurso(self.id)  # Chama o método remoto acessar_recurso
            print(resposta)  # Imprime a resposta recebida do servidor
        except Exception as e:
            print("Falha ao acessar recurso:", e)
            self.iniciar_eleicao(processos)

    def liberar_recurso(self):
        try:
            resposta = self.gerenciador.coordenador_liberar_recurso(self.id)  # Chama o método remoto liberar_recurso
            print(resposta)  # Imprime a resposta recebida do servidor
        except Exception as e:
            print("Falha ao liberar recurso:", e)
            self.iniciar_eleicao(processos)

    def estado_recurso(self):
        try:
            resposta = self.gerenciador.coordenador_estado_recurso()  # Chama o método remoto estado_recurso
            print(resposta)  # Imprime a resposta recebida do servidor
        except Exception as e:
            print("Falha ao verificar estado do recurso:", e)
            self.iniciar_eleicao(processos)

    def listar_fila_espera(self):
        try:
            resposta = self.gerenciador.coordenador_listar_fila_espera()  # Chama o método remoto listar_fila_espera
            print(resposta)  # Imprime a resposta recebida do servidor
        except Exception as e:
            print("Falha ao listar fila de espera:", e)
            self.iniciar_eleicao(processos)

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

    def derrubar_coordenador(self):
        if self.isCoord:
            self.isCoord = False
            return f"simulando queda de coordenador"

    def iniciar_eleicao(self, processos: List['Process']):
        print(f"Processo {self.id} iniciou uma eleição.")
        candidatos = [p for p in processos if p.id > self.id]
        if not candidatos:
            self.isCoord = True
            print(f"Processo {self.id} é o novo coordenador.")
            for p in processos:
                if p.id != self.id:
                    p.notificar_novo_coordenador(self.id)
        else:
            for candidato in candidatos:
                try:
                    resposta = candidato.responder_eleicao(self.id)
                    if resposta == "OK":
                        print(f"Processo {self.id} recebeu resposta de processo {candidato.id}.")
                        candidato.iniciar_eleicao(processos)
                        return
                except:
                    continue

    def responder_eleicao(self, id_processo):
        print(f"Processo {self.id} recebeu uma mensagem de eleição do processo {id_processo}.")
        return "OK"

    def notificar_novo_coordenador(self, id_coordenador):
        print(f"Processo {self.id} foi notificado que o novo coordenador é o processo {id_coordenador}.")
        self.isCoord = False


# Assuming the processes are running on different hosts or different instances
processos = [Process(id=i, isCoord=(i == 1)) for i in range(1, 4)]


def iniciar_servidor(gerenciador: 'Process'):
    daemon = Pyro5.api.Daemon(host="localhost", port=9090)  # Cria um daemon Pyro que escuta na porta 9090 no localhost
    uri = daemon.register(gerenciador, "gerenciador.concorrencia")  # Registra o objeto no daemon com um nome específico
    print(f"Servidor disponível. URI: {uri}")  # Imprime a URI do objeto para facilitar o acesso pelo cliente
    daemon.requestLoop()  # Entra no loop de requisições para processar chamadas remotas


if __name__ == "__main__":
    # Simulating the main server process that acts as the coordinator
    gerenciador = processos[0]
    gerenciador.isCoord = True
    from threading import Thread

    server_thread = Thread(target=iniciar_servidor, args=(gerenciador,))
    server_thread.start()

    # Simulate the crash of the coordinator after some time
    import time

    time.sleep(10)
    print(gerenciador.derrubar_coordenador())

    # Simulate clients trying to access resources and detect coordinator failure
    time.sleep(1)
    processos[1].acessar_recurso()
    processos[2].acessar_recurso()




