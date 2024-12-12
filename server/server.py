import socket
import threading
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém o valor das variáveis de ambiente HOST e PORT
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

# Verifica se as variáveis de ambiente foram definidas
if HOST is None or PORT is None:
    raise ValueError("HOST and PORT environment variables must be set")

# Converte a variável PORT para inteiro
PORT = int(PORT)

# Função para lidar com a conexão de um cliente
def handle_client(conn, addr):
    print(f"Conexão estabelecida com {addr}")
    try:
        while True:
            # Recebe dados do cliente
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break

            # Exibe o que o servidor recebeu
            print(f"Recebido: {data}")
            # Responde ao cliente
            conn.sendall(f"Recebido: {data}".encode('utf-8'))
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        # Encerra a conexão com o cliente
        print(f"Conexão encerrada com {addr}")
        conn.close()

# Função para iniciar o servidor
def start_server():
    # Cria um socket para o servidor para aceitar conexões de clientes TCP com IPv4
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associa o socket ao endereço e porta especificados
    server_socket.bind((HOST, PORT))
    # Coloca o servidor em modo de escuta
    server_socket.listen()
    print(f"Servidor rodando em {HOST}:{PORT}")

    while True:
        # Aceita uma nova conexão
        conn, addr = server_socket.accept()
        # Cria uma nova thread para lidar com o cliente
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    start_server()
