import json
from pathlib import Path
from datetime import datetime
import os
import torch
from transformers import GPTNeoForCausalLM, AutoTokenizer

BASE_DIR = Path(__file__).parent
RESPOSTAS_PATH = BASE_DIR / "responses.json"
MEMORY_PATH = BASE_DIR / "memory.json"

if not MEMORY_PATH.exists():
    with open(MEMORY_PATH, "w", encoding = "utf-8") as arquivo:
        json.dump([], arquivo, ensure_ascii = False, indent = 4)

if not RESPOSTAS_PATH.exists():
    with open(RESPOSTAS_PATH, "w", encoding = "utf-8") as arquivo:
        json.dump([], arquivo, ensure_ascii = False, indent = 4)
    
    
with open(RESPOSTAS_PATH, "r", encoding = "utf-8") as arquivo:
    RESPOSTAS = json.load(arquivo)
    
def salvar_respostas():
    with open(RESPOSTAS_PATH, "w", encoding = "utf-8") as file:
        json.dump(RESPOSTAS, file, ensure_ascii = False, indent = 4)
    
def responder(texto_usuario : str, contexto = None) -> str:
    texto_usuario = texto_usuario.lower()
    
    for chave, resposta in RESPOSTAS.items():
        if chave in texto_usuario:
            return resposta
    
    resposta_ia = gerar_resposta_ia(texto_usuario)
    registrar_historico("Mafins", resposta_ia)
    return resposta_ia


def aprender(pergunta: str, resposta: str):
    RESPOSTAS[pergunta.lower()] = resposta
    salvar_respostas()
    return f"Aprendi, mestre! Quando vocẽ perguntar '{pergunta}', responderei '{resposta}'"

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
        
MODEL_NAME = "EleutherAI/gpt-neo-125M"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id

model = GPTNeoForCausalLM.from_pretrained(MODEL_NAME)

if getattr(model.config, "pad_token_id", None) is None:
    model.config.pad_token_id = model.config.eos_token_id

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def gerar_resposta_ia(texto_usuario: str, max_tokens = 150):
    
    enc = tokenizer(
        texto_usuario,
        return_tensors = "pt",
        padding = True,
        truncation = True,
        max_length = 512
    )
    
    input_ids = enc["input_ids"].to(device)
    attention_mask = enc["attention_mask"].to(device)
    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask = attention_mask,
            max_new_tokens = max_tokens,
            do_sample = True,
            temperature = 0.7,
            top_p = 0.9,
            pad_token_id = tokenizer.pad_token_id
            
        )
    resposta = tokenizer.decode(output[0], skip_special_tokens = True)
    return resposta