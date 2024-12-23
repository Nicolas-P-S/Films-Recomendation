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
        "userId": lambda x: ", ".join(map(str, x)),#Uni todos os userId
        "tag": lambda x: ", ".join(filter(lambda t: t is not np.nan and str(t).lower() != "nan", x)),#Uni tags sem 'nan'
        "rating": lambda x: ", ".join(map(str, x))#Uni todos os ratings
    }).reset_index()
    df_main['infos'] = df_main["genres"].astype(str) + " " + df_main["tag"].astype(str)
    return df_main

def recomendar_filmes_ml():
    while True:
        conn = sqlite3.connect("login.db")
        cursor = conn.cursor()

        print_favorites_films()
        title = input("\nDigite o nome do filme para basear as recomendações: ")
        
        try:
            cursor.execute("SELECT * FROM films WHERE user_id = ? AND title = ?", (id, title))
            result = cursor.fetchone()
            if not result:
                raise ValueError("Filme não encontrado.")
            
            filme_titulo = result[1]
            os.system("cls")
            break
        except ValueError as ve:
            print(f"ERRO: {ve}")
            pause()
        except Exception as e:
            print("ERRO: FILME INVÁLIDO!")
            pause()
    
    vectorizer = TfidfVectorizer()
    Tfidf = vectorizer.fit_transform(df_main["infos"])
    similarity = cosine_similarity(Tfidf)
    df_sim = pd.DataFrame(similarity, columns=df_main['title'], index=df_main['title'])
    
    try:
        recomendacoes = df_sim[filme_titulo].sort_values(ascending=False).head(10)
        
        print(f"Recomendações baseadas no filme '{filme_titulo}':\n")
        c = 0
        for filme, similaridade in recomendacoes.items():
            c += 1
            print(f"[!] Filme nº{c}:")
            print(f"- Título: {filme}")
            print(f"- Similaridade: {similaridade:.4f}\n")
    except KeyError:
        print(f"ERRO: O filme '{filme_titulo}' não está presente na base de dados para recomendação.")    

def pause():
    input("Pressione qualquer tecla para continuar!")

def pesquisar_filmes(nome_filme, limite=15):
    resultados_substring = df_movies[df_movies['title'].str.contains(nome_filme, case=False, na=False)]
    
    if resultados_substring.empty:
        titulos = df_movies['title'].tolist()
        matches = get_close_matches(nome_filme, titulos, n=limite, cutoff=0.3)
        return df_movies[df_movies['title'].isin(matches)]
    return resultados_substring.values.tolist()

def save_film(user_id, titulo, genero, rating):
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")
    
    cursor.execute("CREATE TABLE IF NOT EXISTS films (user_id INTEGER NOT NULL,title TEXT NOT NULL,genre TEXT NOT NULL,rating FLOAT NOT NULL,FOREIGN KEY (user_id) REFERENCES user(id))")
    
    cursor.execute("INSERT INTO films (user_id, title, genre, rating) VALUES (?, ?, ?, ?)", (user_id, titulo, genero, rating))
    conn.commit()
    conn.close()

def favoritar_filme(user_id):
    while True:
        print("\nPesquise e escolha seus filmes favoritos!")
        nome_filme = input("\nDigite o nome do filme para pesquisar (ou 'sair' para finalizar): ")
        if nome_filme.lower() == "sair":
            break

        resultados = pesquisar_filmes(nome_filme)

        os.system("cls")
        if resultados:
            print("\nFilmes encontrados:")
            for filme in resultados:
                print(f'ID: {filme[0]}, Título: {filme[1]}')

            escolha = input("\nDigite o ID do filme para adicioná-lo aos favoritos (ou 'nenhum' para pular): ")
            if escolha.isdigit():
                escolha = int(escolha)
                filme_escolhido = next((filme for filme in resultados if filme[0] == escolha), None)
                
                if filme_escolhido:
                    while True:
                        os.system("cls")
                        rating = input(f'Digite a nota do filme "{filme_escolhido[1]}" (1-5): ')
                        try:
                            rating = float(rating)  # Tenta converter para float
                            if 1 <= rating <= 5:  # Verifica se está no intervalo
                                save_film(user_id, filme_escolhido[1], filme_escolhido[2], rating)
                                print("Filme adicionado aos favoritos!")
                                break
                            else:
                                print("Digite uma nota válida entre 1 e 5!\n")
                                pause()
                        except ValueError:  # Se a conversão falhar
                            print("Digite uma nota válida entre 1 e 5!\n")
                            pause()
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
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='films'")
    table_exists = cursor.fetchone()

    if table_exists:    
        cursor.execute("select * from films where user_id = ?", (id,))
        retorno=cursor.fetchall()
        if retorno:
            return len(retorno)
    return 0
    
def info_conta(id, usuario, senha):
    print("[!]Id:",id)
    print("[!]usuario:",usuario)
    print("[!]senha:",senha)
    print("[!]quantidade de filmes favoritados:",qtd_favorite_films(),"\n")
    pause()

def print_favorites_films():
    if not os.path.exists("login.db"):
        print("Não existem filmes favoritados pelo usuario!\n")
        pause()
        return 
        
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='films'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("SELECT title, genre FROM films WHERE user_id = ?", (id,))
        retorno = cursor.fetchall()
        if retorno:
            print(f"Filmes favoritos de {usuario}!\n")
            c=0
            for filme in retorno:
                c+=1
                print(f"[!]Filme nº{c}:")
                print(f"-Título: {filme[0]}")
                print(f"-Gênero: {filme[1]}\n")
    else:
        print("ERRO: A tabela 'films' não existe!\n")
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
                print_favorites_films()
                pause()
            case "3":
                info_conta(id, usuario, senha)
            case "4":
                recomendar_filmes_ml()
                pause()
            case "5":
                id, usuario, senha=login.menu()
            case "6":
                print(f"Até a proxima, {usuario}!\n")
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
print("\nCARREGANDO...\n")
df_main=training()
pause()
menu_principal()