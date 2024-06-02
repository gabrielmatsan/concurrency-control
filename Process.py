import Pyro5.api
from typing import List

processes = []  # Global list to keep track of processes for election

@Pyro5.api.expose
class Process:
    def __init__(self, id, uri="PYRO:gerenciador.concorrencia@localhost:9090", isCoord=False):
        self.id = id
        self.uri = uri
        self.gerenciador = None
        self.recurso = None
        self.fila_espera = []
        self.isCoord = isCoord

    def get_gerenciador(self):
        if self.gerenciador is None:
            self.gerenciador = Pyro5.api.Proxy(self.uri)
        return self.gerenciador

    def acessar_recurso(self, client_id):
        try:
            gerenciador = self.get_gerenciador()
            resposta = gerenciador.coordenador_acessar_recurso(client_id)
            print(resposta)
        except Exception as e:
            print("Falha ao acessar recurso:", e)
            self.iniciar_eleicao()

    def liberar_recurso(self, client_id):
        try:
            gerenciador = self.get_gerenciador()
            resposta = gerenciador.coordenador_liberar_recurso(client_id)
            print(resposta)
        except Exception as e:
            print("Falha ao liberar recurso:", e)
            self.iniciar_eleicao()

    def estado_recurso(self):
        try:
            gerenciador = self.get_gerenciador()
            resposta = gerenciador.coordenador_estado_recurso()
            print(resposta)
        except Exception as e:
            print("Falha ao verificar estado do recurso:", e)
            self.iniciar_eleicao()

    def listar_fila_espera(self):
        try:
            gerenciador = self.get_gerenciador()
            resposta = gerenciador.coordenador_listar_fila_espera()
            print(resposta)
        except Exception as e:
            print("Falha ao listar fila de espera:", e)
            self.iniciar_eleicao()

    def coordenador_acessar_recurso(self, client_id):
        if self.recurso is None:
            self.recurso = client_id
            return f"Recurso alocado para o cliente {client_id}"
        else:
            self.fila_espera.append(client_id)
            return f"Recurso já alocado para o cliente {self.recurso}. Cliente {client_id} adicionado à fila de espera"

    def coordenador_liberar_recurso(self, client_id):
        if self.recurso == client_id:
            self.recurso = None
            if self.fila_espera:
                proximo_cliente = self.fila_espera.pop(0)
                self.recurso = proximo_cliente
                return f"Recurso liberado pelo cliente {client_id} e alocado para o cliente {proximo_cliente}"
            return f"Recurso liberado pelo cliente {client_id}. Nenhum cliente na fila de espera"
        else:
            return f"Cliente {client_id} não possui o recurso"

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
            return "simulando queda de coordenador"

    def iniciar_eleicao(self):
        print(f"Processo {self.id} iniciou uma eleição.")
        global processes
        candidatos = [p for p in processes if p.id > self.id]

        higher_process_responded = False
        for candidato in candidatos:
            try:
                resposta = candidato.responder_eleicao(self.id)
                if resposta == "OK":
                    higher_process_responded = True
                    candidato.iniciar_eleicao()
                    break
            except Exception as e:
                print(f"Erro ao responder eleição: {e}")

        if not higher_process_responded:
            self.isCoord = True
            print(f"Processo {self.id} é o novo coordenador.")
            for p in processes:
                if p.id != self.id:
                    p.notificar_novo_coordenador(self.id)

    def responder_eleicao(self, id_processo):
        print(f"Processo {self.id} recebeu uma mensagem de eleição do processo {id_processo}.")
        return "OK"

    def notificar_novo_coordenador(self, id_coordenador):
        print(f"Processo {self.id} foi notificado que o novo coordenador é o processo {id_coordenador}.")
        self.isCoord = False
