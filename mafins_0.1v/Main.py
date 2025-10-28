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
        self.resizable(True, True)
        
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_columnconfigure(0, weight = 1)
        
        BASE_DIR = Path(__file__).parent
        ASSETS_DIR = BASE_DIR / "assets"
        
        self.avatar_user = ctk.CTkImage(
            dark_image = Image.open(ASSETS_DIR / "batman.png"),
            size = (40, 40)
        )
        
        self.avatar_mafins = ctk.CTkImage(
            dark_image = Image.open(ASSETS_DIR / "ironman.png"),
            size = (40, 40)
        )
        
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
        
        wrap_len = max(200, self.winfo_width()-200)
        
        if autor == "Mafins":
            ctk.CTkLabel(container, image = avatar, text = "").pack(side = "left", padx = 6)
            ctk.CTkLabel(
                container,
                text = mensagem,
                justify = "left",
                wraplength = wrap_len,
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
                wraplength = wrap_len,
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

