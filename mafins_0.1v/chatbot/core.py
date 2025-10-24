import json
from pathlib import Path

respostas_path = Path(__file__).parent / "responses.json"

with open(respostas_path, "r", encoding = "utf-8") as arquivo:
    RESPOSTAS = json.load(arquivo)
    
def responder(texto_usuario : str) -> str:
    texto_usuario = texto_usuario.lower()
    
    for chave, resposta in RESPOSTAS.items():
        if chave in texto_usuario:
            return resposta
    
    return "Desculpa, mestre. Não aprendi a responder essa pergunta ainda"

