import customtkinter as ctk

def criar_balao_de_mensagem(
    parent,
    autor: str,
    mensagem: str,
    avatar_user,
    avatar_mafins,
    largura_de_janela: int,
    font_size: int
):
    mensagem_frame = ctk.CTkFrame(parent, corner_radius = 12, fg_color = "transparent")
    mensagem_frame.columnconfigure(0, weight = 1)
    
    if autor == "Você":
        avatar = avatar_user
        bubble_color = "#3BA55D"
        text_justify = "right"
        avatar_col = 1
        bubble_col = 0
        sticky = "e"
        
    else:
        avatar = avatar_mafins
        bubble_color = "#0078D7"
        text_justify = "left"
        avatar_col = 0
        bubble_col = 1
        sticky = "w"
    
    container = ctk.CTkFrame(mensagem_frame, fg_color = "transparent")
    container.grid(row = 0, column = 0, sticky = sticky, padx = 10, pady = 4)
    container.columnconfigure(0, weight = 0)
    container.columnconfigure(1, weight = 1)
    
    avatar_label = ctk.CTkLabel(container, image = avatar, text = "")
    avatar_label.grid(row = 0, column = avatar_col, padx = 6, sticky = sticky)
        
    wrap_len = max(200, largura_de_janela-200)
        
    bubble = ctk.CTkLabel(
        container,
        text = mensagem,
        justify = text_justify,
        wraplength = wrap_len,
        corner_radius = 10,
        fg_color = bubble_color,
        text_color = "white",
        font = ("Arial", font_size),
        padx = 10,
        pady = 6
    )
    bubble.grid(row = 0, column = bubble_col, sticky = sticky, padx = 6)
        
    mensagem_frame.bubble = bubble
    
    return mensagem_frame

