import asyncio
import socket
import yt_dlp
from discord import FFmpegOpusAudio
from dotenv import load_dotenv
import os
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DiscordBot")

# Carregar variáveis de ambiente
load_dotenv()
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

# Opções para o FFmpeg
ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": '-vn -filter:a "volume=0.25"'
}
ffmpeg_options_mp3 = {'options': '-vn -filter:a "volume=0.15"'}

# Função para conectar o bot ao canal de voz do autor da mensagem
async def join_channel(message):
    """Conecta o bot ao canal de voz do autor da mensagem."""
    logger.info("Tentando entrar no canal de voz...")
    if message.author.voice:
        channel = message.author.voice.channel
        logger.info(f"Entrando no canal de voz: {channel.name}")
        try:
            await channel.connect()
            await message.channel.send("Entrei no canal de voz!")
        except Exception as e:
            logger.error(f"Erro ao tentar entrar no canal de voz: {e}")
            await message.channel.send(f"Erro ao tentar entrar no canal de voz: {e}")
    else:
        await message.channel.send("Você precisa estar em um canal de voz.")

# Função para desconectar o bot do canal de voz
async def leave_channel(message):
    """Desconecta o bot do canal de voz."""
    voice_client = message.guild.voice_client
    if voice_client:
        await voice_client.disconnect()
        await message.channel.send("Saí do canal de voz.")
    else:
        await message.channel.send("Não estou em um canal de voz.")

# Função para solicitar informações sobre a música a um servidor via socket
def request_music(source, query):
    """Solicita informações sobre a música a um servidor via socket."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(f"{source}:{query}".encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
        return response
    except Exception as e:
        logger.error(f"Erro ao solicitar música via socket: {e}")
        return None

# Função para tocar uma música no canal de voz
async def play_music(message, query):
    """Toca uma música no canal de voz."""
    voice_client = message.guild.voice_client
    if voice_client is None:
        await message.channel.send("Eu não estou em um canal de voz.")
        return

    if not hasattr(voice_client, 'queue'):
        voice_client.queue = []

    if voice_client.is_playing():
        voice_client.queue.append(query)
        await message.channel.send(f"A música {query} foi adicionada à fila.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': '-',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(query, download=False)
            audio_url = info_dict.get('url')
            title = info_dict.get('title', 'Desconhecido')

            if not audio_url:
                raise ValueError("URL de áudio não encontrada.")

            audio_source = FFmpegOpusAudio(audio_url, **ffmpeg_options)
            voice_client.play(
                audio_source,
                after=lambda e: on_music_end(voice_client, message)
            )

            await message.channel.send(f"Tocando: {title}")

    except Exception as e:
        await message.channel.send(f"Ocorreu um erro ao tentar tocar a música: {e}")
        logger.error(f"Erro ao tocar música: {e}")

# Função callback executada quando uma música termina
def on_music_end(voice_client, message):
    """Callback executado quando uma música termina."""
    if hasattr(voice_client, 'queue') and voice_client.queue:
        next_song = voice_client.queue.pop(0)
        logger.info(f"Reproduzindo próxima música da fila: {next_song}")
        # Como esta função é chamada de forma assíncrona, é necessário agendar a execução
        coro = play_music(message, next_song)
        asyncio.run_coroutine_threadsafe(coro, message.guild.voice_client.loop)
    else:
        logger.info("Fila vazia, nenhuma música para tocar.")

# Função para parar a música que está sendo tocada
async def stop_music(message):
    """Para a música que está sendo tocada."""
    voice_client = message.guild.voice_client
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await message.channel.send("Música parada.")
    else:
        await message.channel.send("Não há música tocando no momento.")

# Função para pular a música atual e tocar a próxima da fila, se disponível
async def skip_music(message):
    """Pula a música atual e toca a próxima da fila, se disponível."""
    voice_client = message.guild.voice_client
    if voice_client is None:
        await message.channel.send("Eu não estou em um canal de voz.")
        return

    if voice_client.is_playing():
        voice_client.stop()
        if hasattr(voice_client, 'queue') and voice_client.queue:
            next_song = voice_client.queue.pop(0)
            await play_music(message, next_song)
        else:
            await message.channel.send("Não há mais músicas na fila.")
    else:
        await message.channel.send("Não há música tocando no momento.")
