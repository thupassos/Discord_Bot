from music import join_channel, leave_channel, play_music, stop_music, skip_music
import re

async def handle_commands(client, message):
    print(f"Comando recebido: {message.content}")  # Log de depuração
    
    # Remover a menção ao bot, caso exista
    command_content = re.sub(r'<@!?(\d+)>', '', message.content).strip()
    
    print(f"Comando limpo: {command_content}")  # Log de depuração

    if command_content.startswith('!join'):
        print("Comando !join detectado")
        await join_channel(message)
    elif command_content.startswith('!leave'):
        print("Comando !leave detectado") 
        await leave_channel(message)
    elif command_content.startswith('!play'):
        print("Comando !play detectado")  
        search_query = command_content[len('!play '):]
        await play_music(message, search_query)
    elif command_content.startswith('!stop'):
        print("Comando !stop detectado")  
        await stop_music(message)
    elif command_content.startswith('!skip'):
        await skip_music(message)
        print("Comando !skip detectado")  


