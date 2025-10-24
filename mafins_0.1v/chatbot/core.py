import json
from pathlib import Path
from datetime import datetime

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
    with open(MEMORY_PATH, "r", encoding = "utf-8") as arquivo:
        historico = json.load(arquivo)
        
    historico.append({
        "Autor": autor,
        "Mensagem": mensagem,
        "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    with open(MEMORY_PATH, "w", encoding = "utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii = False, indent = 4)