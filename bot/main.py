import discord
from commands import handle_commands
from dotenv import load_dotenv
import os
import socket

# Define as intenções do bot, permitindo que ele leia mensagens
intents = discord.Intents.default()
intents.messages = True 

# Cria uma instância do cliente do Discord com as intenções definidas
client = discord.Client(intents=intents)

#Carrega HOST e PORT do arquivo .env
load_dotenv()
HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

    # Cria um socket para o servidor para aceitar conexões de clientes TCP com IPv4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

@client.event
async def on_ready():
    print(f"Bot conectado como {client.user}")

@client.event
async def on_message(message):
    print(f"Mensagem recebida: {message.content}")  # Log para depuração
    
    if message.author == client.user:
        return  # Ignora as mensagens do próprio bot
    
    #Envia o conteúdo da mensagem para o servidor
    sock.sendall(message.content.encode('utf-8'))
    
    #Recebe a resposta do servidor
    data = sock.recv(1024)
    print(f"Recebido do servidor: {data.decode('utf-8')}")
    
    await handle_commands(client, message)

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")
    client.run(TOKEN)
