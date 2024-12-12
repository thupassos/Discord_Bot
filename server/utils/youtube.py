import re
import requests

def search_youtube(query):
    # Monta a URL de busca do YouTube com a query fornecida
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    
    # Faz uma requisição GET para a URL de busca
    response = requests.get(search_url)
    
    # Usa expressão regular para encontrar todos os IDs de vídeo na resposta HTML
    video_ids = re.findall(r"watch\?v=(\S{11})", response.text)
    
    # Se encontrar IDs de vídeo, retorna o link do primeiro vídeo encontrado
    if video_ids:
        return f"https://www.youtube.com/watch?v={video_ids[0]}"
    
    # Se não encontrar nenhum vídeo, retorna uma mensagem de vídeo não encontrado
    return "Vídeo não encontrado."
