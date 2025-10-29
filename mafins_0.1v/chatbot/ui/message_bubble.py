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
    
    if autor == "Você":
        avatar = avatar_user
        bubble_color = "#3BA55D"
        coluna_avatar = 2
        coluna_bubble = 1
        anchor = "e"
        justify = "right"
        
    else:
        avatar = avatar_mafins
        bubble_color = "#0078D7"
        coluna_avatar = 0
        coluna_bubble = 1
        anchor = "w"
        justify = "left"
    
    container = ctk.CTkFrame(mensagem_frame, fg_color = "transparent")
    container.grid(sticky =  anchor, padx = 10, pady = 4)
        
    wrap_len = max(200, largura_de_janela-200)

    if autor == "Mafins":
        ctk.CTkLabel(container, image = avatar, text = "").grid(row = 0, column = coluna_avatar, padx = 6, sticky = "w")
        
    bubble = ctk.CTkLabel(
        container,
        text = mensagem,
        justify = justify,
        wraplength = wrap_len,
        corner_radius = 10,
        fg_color = bubble_color,
        text_color = "white",
        font = ("Arial", font_size),
        padx = 10,
        pady = 6
    )
    bubble.grid(row = 0, column = coluna_bubble, sticky = anchor)
    
    if autor != "Mafins":
        ctk.CTkLabel(container, image = avatar, text = "").grid(row = 0, column = coluna_avatar, padx = 6, sticky = "e")
    
    container.grid_columnconfigure(0, weight = 1)
    container.grid_columnconfigure(1, weight = 0)
    container.grid_columnconfigure(2, weight = 1)
        
    mensagem_frame.grid(sticky = anchor, padx = 20, pady = 4)
    
    return mensagem_frame
