from difflib import get_close_matches
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import login
import os
import sqlite3

def training():
    df_main=pd.merge(df_movies, df_ratings, on="movieId", how="inner")
    df_main=pd.merge(df_main, df_tags, on=["movieId", "userId"], how="left")
    df_main = df_main.groupby(["movieId", "title", "genres"]).agg({
        "userId": lambda x: ", ".join(map(str, x)),      # Juntar todos os userId
        "tag": lambda x: ", ".join(filter(lambda t: t is not np.nan and str(t).lower() != "nan", x)),  # Juntar tags sem 'nan'
        "rating": lambda x: ", ".join(map(str, x))
    }).reset_index()
    df_main['infos'] = df_main["genres"].astype(str) + " " + df_main["tag"].astype(str)
    return df_main

def recomendar_filmes_ml(titulo):
    vectorizer = TfidfVectorizer()
    Tfidf = vectorizer.fit_transform(df_main["infos"])
    similarity = cosine_similarity(Tfidf)
    df_sim=pd.DataFrame(similarity, columns=df_main['title'], index=df_main['title'])
    teste=pd.DataFrame(df_sim[titulo].sort_values(ascending=False))
    print(teste.head())

def pause():
    input("Pressione qualquer tecla para continuar!")

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
    filmes_favoritos = []

    while True:
        print("\nPesquise e escolha seus filmes favoritos!")
        nome_filme = input("\nDigite o nome do filme para pesquisar (ou 'sair' para finalizar): ")
        if nome_filme.lower() == "sair":
            break

        # Buscar filmes no dataframe
        resultados = pesquisar_filmes(nome_filme)

        os.system("cls")
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
            os.system("cls")
        else:
            print("Nenhum filme encontrado com esse nome ou similaridade.")

def qtd_favorite_films():
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    
    cursor.execute("select * from films where user_id = ?", (id,))
    retorno=cursor.fetchall()
    
    if retorno:
        return len(retorno)
    else:
        return 0
    
def info_conta(id, usuario, senha):
    print("[!]Id:",id)
    print("[!]usuario:",usuario)
    print("[!]senha:",senha)
    print("[!]quantidade de filmes favoritados:",qtd_favorite_films(),"\n")
    pause()

def print_favorites_films(user_id):
    if not os.path.exists("login.db"):
        print("Não existem filmes favoritados pelo usuario!\n")
        pause()
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
        pause()
    else:
        input("Não existem filmes favoritados pelo usuario!\n")
        pause()

def menu_principal():
    global id, usuario, senha
    while True:
        os.system("cls")
        print("[!] Escolha uma opção:\n")
        print("[1]: Favorite um filme")
        print("[2]: Listar Filmes favoritos")
        print("[3]: Informações da conta")
        print("[4]: Recomendar filmes")
        print("[5]: Mudar usuário")
        print("[6]: Sair")
        escolha = input("=> ")
        os.system("cls")
        
        match escolha:
            case "1":
                favoritar_filme(id)
            case "2":
                print_favorites_films(id)
            case "3":
                info_conta(id, usuario, senha)
            case "4":
                recomendar_filmes_ml("Lord of the Rings, The (1978)")
                pause()
            case "5":
                id, usuario, senha=login.menu()
            case "6":
                input(f"Até a proxima, {usuario}!\n")
                pause()
                break
            case _:
                input("Tecla inválida!")

# Carregar os dados
df_links = pd.read_csv("ml-latest-small/links.csv")
df_movies = pd.read_csv("ml-latest-small/movies.csv")
df_ratings = pd.read_csv("ml-latest-small/ratings.csv")
df_tags = pd.read_csv("ml-latest-small/tags.csv")

global id, usuario, senha
id, usuario, senha=login.menu()
df_main=training()

menu_principal()