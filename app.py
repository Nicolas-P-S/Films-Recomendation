import pandas as pd
from difflib import get_close_matches
import login
import os
import sqlite3

def pesquisar_filmes(nome_filme, limite=15):
    """
    Pesquisa filmes pelo nome parcial ou similar.
    """
    # Filmes que contêm o termo digitado (ignora maiúsculas/minúsculas)
    resultados_substring = df_movies[df_movies['title'].str.contains(nome_filme, case=False, na=False)]
    
    # Se não encontrar diretamente, usa similaridade como fallback
    if resultados_substring.empty:
        titulos = df_movies['title'].tolist()
        matches = get_close_matches(nome_filme, titulos, n=limite, cutoff=0.3)
        return df_movies[df_movies['title'].isin(matches)]
    return resultados_substring.values.tolist()

def save_film(user_id, titulo, genero):
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    
    # Ativar o suporte a chaves estrangeiras
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Criar a tabela de filmes, se não existir
    cursor.execute("CREATE TABLE IF NOT EXISTS films (user_id INTEGER NOT NULL,title TEXT NOT NULL,genre TEXT NOT NULL,FOREIGN KEY (user_id) REFERENCES user(id))")
    
    # Inserir o filme vinculado ao usuário
    cursor.execute("INSERT INTO films (user_id, title, genre) VALUES (?, ?, ?)", (user_id, titulo, genero))
    conn.commit()
    conn.close()

def favoritar_filme(user_id):
    #Selecionar filmes favoritos
    print("\nPesquise e escolha seus filmes favoritos!")
    filmes_favoritos = []

    while True:
        nome_filme = input("\nDigite o nome do filme para pesquisar (ou 'sair' para finalizar): ")
        if nome_filme.lower() == "sair":
            break

        # Buscar filmes no dataframe
        resultados = pesquisar_filmes(nome_filme)

        if resultados:
            print("\nFilmes encontrados:")
            for filme in resultados:
                print(f'ID: {filme[0]}, Título: {filme[1]}')

            escolha = input("\nDigite o ID do filme para adicioná-lo aos favoritos (ou 'nenhum' para pular): ")
            if escolha.isdigit():
                escolha = int(escolha)
                # Verificar se o ID existe na lista de resultados
                filme_escolhido = next((filme for filme in resultados if filme[0] == escolha), None)
                
                if filme_escolhido:
                    filmes_favoritos.append(escolha)
                    save_film(user_id, filme_escolhido[1], filme_escolhido[2])
                    print("Filme adicionado aos favoritos!")
                else:
                    print("ID inválido ou nenhum filme encontrado com esse ID.")
            else:
                print("Entrada inválida. Por favor, insira um número.")
        else:
            print("Nenhum filme encontrado com esse nome ou similaridade.")

def info_conta(id, usuario, senha):
    print("[!]Id:",id)
    print("[!]usuario:",usuario)
    print("[!]senha:",senha)
    print("[!]quantidade de filmes favoritados:")
    input("\nPressione Enter para continuar...")

def print_favorites_films(user_id):
    if not os.path.exists("login.db"):
        input("Não existem filmes favoritados pelo usuario!")
        return 
        
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()

    cursor.execute("select title, genre from films where user_id = (?)", (user_id,))
    retorno = cursor.fetchall()
    
    if retorno:
        print(f"Filmes favoritos de {usuario}!\n")
        c=0
        for filme in retorno:
            c+=1
            print(f"[!]Filme nº{c}:")
            print(f"-titulo: {filme[0]}")
            print(f"-genero: {filme[1]}\n")
        input()
    else:
        input("Não existem filmes favoritados pelo usuario!")

def menu_principal(): 
    while True:
        os.system("cls")
        print("[!] Escolha uma opção:\n")
        print("[1]: Favorite um filme")
        print("[2]: Listar Filmes favoritos")
        print("[3]: Informações da conta")
        print("[4]: Recomendar filmes")
        print("[5]: Mudar usuário")
        print("[6]: Sair")
        escolha = int(input("=> "))
        os.system("cls")
        
        match escolha:
            case 1:
                favoritar_filme(id)
            case 2:
                print_favorites_films(id)
            case 3:
                info_conta(id, usuario, senha)
            case 4:
                pass
            case 5:
                pass
            case 6:
                input(f"Até a proxima, {usuario}!")
                break
            case _:
                pass

# Carregar os dados
df_links = pd.read_csv("ml-latest-small/links.csv")
df_movies = pd.read_csv("ml-latest-small/movies.csv")
df_ratings = pd.read_csv("ml-latest-small/ratings.csv")
df_tags = pd.read_csv("ml-latest-small/tags.csv")

id, usuario, senha=login.menu()

menu_principal()