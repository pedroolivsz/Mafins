import customtkinter as ctk
from chatbot.core import responder, registrar_historico

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MafinsChat(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        self.title("Mafins - Chatbot")
        self.geometry("500x600")
        self.resizable(False, False)
        
        chat_frame = ctk.CTkFrame(self)
        chat_frame.pack(padx = 10, pady = 10, fill = "both", expand = True)
        
        self.chat_display = ctk.CTkTextbox(chat_frame, width = 480, height = 450, state = "disabled", wrap = "word")
        self.chat_display.pack(side = "left", fill = "both", expand = True)
        
        self.scrollbar = ctk.CTkScrollbar(chat_frame, orientation = "vertical", command = self.chat_display.yview)
        self.scrollbar.pack(side = "right", fill = "y")
        self.chat_display.configure(yscrollcommand = self.scrollbar.set)
        
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
            
            resposta = responder(user_text)
            self.exibir_mensagem("Mafins", resposta)
            
            registrar_historico("Você", user_text)
            registrar_historico("Mafins", resposta)
            
    def exibir_mensagem(self, autor, mensagem):
        self.chat_display.configure(state = "normal")
        self.chat_display.insert("end", f"{autor}: {mensagem}\n")
        self.chat_display.configure(state = "disabled")
        self.chat_display.see("end")

if __name__ == "__main__":
    app = MafinsChat()
    app.mainloop()

