import customtkinter as ctk
from chatbot.core import responder, registrar_historico
from PIL import Image
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MafinsChat(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Mafins - Chatbot")
        self.geometry("500x600")
        self.resizable(False, False)
        
        BASE_DIR = Path(__file__).parent
        ASSETS_DIR = BASE_DIR / "assets"
        
        self.avatar_user = ctk.CTkImage(
            light_image = Image.open(ASSETS_DIR / "batman.png"),
            dark_image = Image.open(ASSETS_DIR / "batman.png"),
            size = (40, 40)
        )
        
        self.avatar_mafins = ctk.CTkImage(
            light_image = Image.open(ASSETS_DIR / "ironman.png"),
            dark_image = Image.open(ASSETS_DIR / "ironman.png"),
            size = (40, 40)
        )
        
        self.chat_frame = ctk.CTkScrollableFrame(self, width = 480, height = 450)
        self.chat_frame.pack(padx = 10, pady = 10, fill = "both", expand = True)
        
        frame_input = ctk.CTkFrame(self)
        frame_input.pack(fill = "x", padx = 10, pady = 10)
        
        self.entry = ctk.CTkEntry(self, width = 400, placeholder_text = "Digite algo...")
        self.entry.pack(side = "left", padx = (10, 0), pady = (0, 10))
        self.entry.bind("<Return>", lambda event: self.enviar_mensagem())
        
        self.send_button = ctk.CTkButton(frame_input, text = "Enviar", command = self.enviar_mensagem)
        self.send_button.pack(side = "right")
        
    def enviar_mensagem(self):
        user_text = self.entry.get().strip()
        if user_text:
            self.entry.delete(0, "end")
            self.exibir_mensagem("Você", user_text)
            registrar_historico("Você", user_text)
            
            resposta = responder(user_text)
            self.exibir_mensagem("Mafins", resposta)
            registrar_historico("Mafins", resposta)
            
    def exibir_mensagem(self, autor, mensagem):
        msg_frame = ctk.CTkFrame(self.chat_frame, corner_radius = 12, fg_color = "transparent")
        
        if autor == "Você":
            avatar = self.avatar_user
            bubble_color = "#2E8B57"
            anchor = "e"
        
        else:
            avatar = self.avatar_mafins
            bubble_color = "#1E90FF"
            anchor = "w"
        
        container = ctk.CTkFrame(msg_frame, fg_color = "transparent")
        container.pack(fill = "x", pady = 4)
        
        if autor == "Mafins":
            ctk.CTkLabel(container, image = avatar, text = "").pack(side = "left", padx = 6)
            ctk.CTkLabel(
                container,
                text = mensagem,
                justify = "left",
                wraplength = 300,
                corner_radius = 10,
                fg_color = bubble_color,
                text_color = "white",
                padx = 10,
                pady = 10
            ).pack(side = "left", padx = 6)
        else:
            ctk.CTkLabel(
                container,
                text = mensagem,
                justify = "right",
                wraplength = 300,
                corner_radius = 10,
                fg_color = bubble_color,
                text_color = "white",
                padx = 10,
                pady = 6
            ).pack(side = "right", padx = 5)
            ctk.CTkLabel(container, image = avatar, text = "").pack(side = "right", padx = 6)
        
        msg_frame.pack(fill = "x", anchor = anchor, padx = 5)
        self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = MafinsChat()
    app.mainloop()

