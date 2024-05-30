import Process

if __name__ == "__main__":
    process1 = Process.Process(1)  # Cria um cliente com ID "cliente1"
    process2 = Process.Process(2)  # Cria um cliente com ID "cliente2"
    process3 = Process.Process(3)  # Cria um cliente com ID "cliente3"
    
    process1.acessar_recurso()  # Cliente tenta acessar o recurso
    process2.acessar_recurso()  # Cliente tenta acessar o recurso
    process3.acessar_recurso()
    process1.estado_recurso()  # Cliente verifica o estado do recurso
    process1.listar_fila_espera()  # Cliente lista os clientes na fila de espera
    process1.liberar_recurso()  # Cliente tenta liberar o recurso    
    process2.estado_recurso()  # Cliente verifica o estado do recurso
    process2.listar_fila_espera()  # Cliente lista os clientes na fila de espera
    process2.liberar_recurso()  # Cliente tenta liberar o recurso

