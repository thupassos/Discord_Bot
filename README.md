# Discord Music Bot

🎵 Este projeto é um bot para Discord que oferece funcionalidades de reprodução de músicas em canais de voz, como tocar, pausar, parar, pular faixas, e gerenciar filas de músicas. Além disso, inclui integração com um servidor socket para troca de mensagens e execução de comandos. 🎶🎧

## Funcionalidades

- **Conexão com canais de voz:** O bot pode se conectar e desconectar de canais de voz no Discord. 🎤
- **Reprodução de músicas:** Suporte a músicas extraídas do YouTube usando `yt-dlp`. 📀
- **Fila de músicas:** Gerenciamento de filas para reprodução sequencial. 🗂️
- **Comandos via Discord:** Controle completo por mensagens no canal de texto. 💬
- **Servidor Socket:** Interação bidirecional entre o cliente e o servidor socket. 🌐

## Requisitos

- Python 3.9 ou superior.
- Dependências listadas no arquivo `requirements.txt`.
- FFmpeg instalado e configurado no PATH do sistema.
- Um servidor Discord com permissões adequadas para o bot. 🛠️

## Instalação

1. **Clone o repositório:**

   
   git clone <URL_DO_REPOSITORIO>
   cd DiscordBot
   

2. **Crie e ative um ambiente virtual:**

   
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate  # Para Windows
   

3. **Instale as dependências:**

   
   pip install -r requirements.txt
   

4. **Configure o arquivo ********`.env`********:**
   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis de ambiente:

   env
   DISCORD_TOKEN=SEU_TOKEN_DISCORD
   HOST=127.0.0.1
   PORT=PORTA_DISPONIVEL
   

5. **Instale o FFmpeg:**

   - **Windows:**

     1. Baixe o FFmpeg do site oficial: [FFmpeg Downloads](https://ffmpeg.org/download.html).
     2. Extraia os arquivos em um diretório de sua escolha.
     3. Adicione o caminho da pasta `bin` do FFmpeg nas variáveis de ambiente do sistema (`PATH`).

   - **Linux:**

     
     sudo apt update
     sudo apt install ffmpeg
     

   - **Mac:**

     
     brew install ffmpeg
     

6. **Inicie o servidor:**
   Execute o servidor socket em uma aba do terminal:

   
   python server.py
   

7. **Inicie o bot:**
   Em outra aba do terminal, execute o bot:

   
   python bot.py
   

## Comandos Disponíveis

### Comandos de Voz

- **`!join`**: Conecta o bot ao canal de voz do usuário. 🎙️
- **`!leave`**: Desconecta o bot do canal de voz. 🚪
- **`!play <URL/termo de busca>`**: Reproduz uma música a partir de um link ou termo de busca no YouTube. 🎵
- **`!stop`**: Para a música atual. ⏹️
- **`!skip`**: Pula para a próxima música na fila. ⏭️

### Comandos Gerais

- Mensagens enviadas são tratadas pelo servidor socket para respostas dinâmicas. 📡

## Estrutura do Projeto


DiscordBot/
├── bot/                  # Diretório principal do bot
│   ├── commands.py       # Lógica para lidar com os comandos
│   ├── main.py           # Arquivo de execução principal
│   ├── music.py          # Funções relacionadas à reprodução de música
├── server/               # Diretório relacionado ao servidor socket
│   ├── server.py         # Implementação do servidor socket
│   ├── utils/            # Utilitários e módulos auxiliares
│       ├── youtube.py    # Função para buscar vídeos no YouTube
├── requirements.txt      # Dependências do projeto
├── .env                  # Variáveis de ambiente
└── README.md             # Documentação do projeto



## Tecnologias Utilizadas

- **Linguagem:** Python 🐍
- **Bibliotecas:**
  - `discord.py`: Integração com a API do Discord.
  - `yt-dlp`: Extração de áudio e vídeos do YouTube.
  - `requests`: Realização de requisições HTTP, como pesquisa no YouTube.
  - `pydub`: Manipulação de arquivos de áudio.
  - `aiohttp`: Requisições assíncronas e suporte a downloads.
  - `python-dotenv`: Gerenciamento de variáveis de ambiente.
  - `PyNaCl`: Suporte para codecs de áudio do Discord.
  - `socket`: Comunicação cliente-servidor.
- **FFmpeg:** Para processamento de áudio. 🎛️

## Contribuição

Sinta-se à vontade para abrir problemas (issues) ou enviar pull requests para melhorias e correções. 🤝

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE). 📜

---

Se tiver dúvidas ou problemas, entre em contato! ✉️

