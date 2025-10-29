import customtkinter as ctk
from chatbot.core import responder, registrar_historico, aprender
from chatbot.ui.message_bubble import criar_balao_de_mensagem
from collections import deque
from PIL import Image
from pathlib import Path

class MafinsChat(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Mafins - ChatBot")
        self.geometry("500x600")
        self.resizable(True, True)
        self.modo_aprendizado = False
        self.ultima_pergunta = ""
        self.contexto = deque(maxlen = 5)
        
        self.configurar_layout()
        self.carregar_avatares()
        self.criar_widgets()
    
    def configurar_layout(self):
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_columnconfigure(0, weight = 1)
    
    def carregar_avatares(self):
        ASSETS_DIRECTORY = Path(__file__).parent / "assets"
        self.avatar_user = ctk.CTkImage(Image.open(ASSETS_DIRECTORY / "batman.png"), size = (40, 40))
        self.avatar_mafins = ctk.CTkImage(Image.open(ASSETS_DIRECTORY / "ironman.png"), size = (40, 40))
    
    def criar_widgets(self):
        self.chat_frame = ctk.CTkScrollableFrame(self)
        self.chat_frame.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
        
        frame_input = ctk.CTkFrame(self)
        frame_input.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "ew")
        frame_input.columnconfigure(0, weight = 1)
        frame_input.columnconfigure(1, weight = 0)
        
        self.entry = ctk.CTkEntry(frame_input, placeholder_text = "Digite algo...")
        self.entry.grid(row = 0, column = 0, padx = (0, 8), pady = (5, 5), sticky = "ew")
        self.entry.bind("<Return>", lambda event: self.enviar_mensagem())
        
        self.send_button = ctk.CTkButton(frame_input, text = "Enviar", command = self.enviar_mensagem)
        self.send_button.grid(row = 0, column = 1, pady = (5, 5))
        
        self.message_labels = []
        
        self.bind("<Configure>", self._on_resize)
    
    def enviar_mensagem(self):
        user_text = self.entry.get().strip()
        
        if not user_text:
            return
        
        self.entry.delete(0, "end")
        self._registrar_mensagem("Você", user_text)
        
        if self.modo_aprendizado:
            resposta_correta = user_text
            confirmacao = aprender(self.ultima_pergunta, resposta_correta)
            self._registrar_mensagem("Mafins", confirmacao)
            self.modo_aprendizado = False
            self.ultima_pergunta = ""
            return
            
        resposta = responder(user_text)
        self._registrar_mensagem("Mafins", resposta)
        
        if "quer me ensinar" in resposta.lower():
            self.modo_aprendizado = True
            self.ultima_pergunta = user_text
            self.exibir_mensagem("Mafins", "Digite agora o que posso responder da proxima vez.")
    
    def _registrar_mensagem(self, autor, mensagem):
        self.exibir_mensagem(autor, mensagem)
        registrar_historico(autor, mensagem)
        self.contexto.append({"Autor": autor, "mensagem": mensagem})
        
    def exibir_mensagem(self, autor, mensagem):
        bubble = criar_balao_de_mensagem(
            parent = self.chat_frame,
            autor = autor,
            mensagem = mensagem,
            avatar_user = self.avatar_user,
            avatar_mafins = self.avatar_mafins,
            largura_de_janela = self.winfo_width(),
            font_size = self._get_dynamic_font_size()
        )
        self.after(100, lambda: self.scroll_to_bottom())
        self.message_labels.append(bubble)
    
    def scroll_to_bottom(self):
        try:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        except AttributeError:
            pass
    
    def _get_dynamic_font_size(self):
        width = self.winfo_width()
        if width < 450:
            return 11
        elif width < 700:
            return 13
            
        return 15

    def _on_resize(self, event):
        new_wrap = max(200, self.winfo_width()-220)
        font_size = self._get_dynamic_font_size()
            
        for bubble in self.message_labels:
            bubble.configure(wraplength = new_wrap, font = ("Arial", font_size))