import customtkinter as ctk
from chatbot.ui.main_window import MafinsChat

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = MafinsChat()
    app.mainloop()