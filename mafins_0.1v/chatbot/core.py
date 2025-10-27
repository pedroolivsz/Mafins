import json
from pathlib import Path
from datetime import datetime
import os

BASE_DIR = Path(__file__).parent
RESPOSTAS_PATH = BASE_DIR / "responses.json"
MEMORY_PATH = BASE_DIR / "memory.json"

if not MEMORY_PATH.exists():
    with open(MEMORY_PATH, "w", encoding = "utf-8") as arquivo:
        json.dump([], arquivo, ensure_ascii = False, indent = 4)

if not MEMORY_PATH.exists():
    with open(MEMORY_PATH, "w", encoding = "utf-8") as arquivo:
        json.dump([], arquivo, ensure_ascii = False, indent = 4)
    
    
with open(RESPOSTAS_PATH, "r", encoding = "utf-8") as arquivo:
    RESPOSTAS = json.load(arquivo)
    
def responder(texto_usuario : str) -> str:
    texto_usuario = texto_usuario.lower()
    
    for chave, resposta in RESPOSTAS.items():
        if chave in texto_usuario:
            return resposta
    
    return "Desculpa, mestre. Não aprendi a responder essa pergunta ainda"

def registrar_historico(autor: str, mensagem: str):
    
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w", encoding = "utf-8") as file:
            json.dump([], file)
            
    try:
        
        with open(MEMORY_PATH, "r", encoding = "utf-8") as file:
            conteudo = file.read().strip()
            if not conteudo:
                historico = []
            else:
                historico = json.loads(conteudo)
                
    except (json.JSONDecodeError, FileNotFoundError):
        historico = []
        
    historico.append({
        "Autor": autor,
        "Mensagem": mensagem,
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(MEMORY_PATH, "w", encoding = "utf-8") as file:
        json.dump(historico, file, ensure_ascii = False, indent = 4)