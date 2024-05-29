# saved as client.py
import Pyro5.api

# Criação do proxy para o servidor Kerberos
kerberos = Pyro5.api.Proxy("PYRONAME:example.kerb")    # use name server object lookup uri shortcut

# Solicitação de nome do usuário
name = input("What is your name? ").strip()
print(kerberos.get_fortune(name))

# Solicitação de entrada para a e b e cálculo da soma
a, b = input("Enter 'a', 'b' to get its sum ").split(' ')
print(kerberos.sum(a, b))

# Listagem de arquivos no servidor
print("Files under Server\n")
print(kerberos.listdir())

# Solicitação do nome do arquivo para transferência
fname = input("Enter filename to transfer ").strip()
x = kerberos.sendfile(fname)
if x:
    with open('./Client/' + str(fname), 'w') as f:
        f.write(kerberos.sendfile(fname))
    print(f"File {fname} transferred successfully.")
else:
    print("File not found")
