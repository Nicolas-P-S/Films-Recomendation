import pandas as pd
from difflib import get_close_matches
import login
import os

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
    retorno = resultados_substring[['movieId', 'title']]
    return retorno.values.tolist()

def favoritar_filme():
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
            if escolha.isdigit() and int(escolha) in (filme[0] for filme in resultados):
                filmes_favoritos.append(int(escolha))
                print("Filme adicionado aos favoritos!")
            else:
                print("ID inválido ou nenhum filme selecionado.")
        else:
            print("Nenhum filme encontrado com esse nome ou similaridade.")

def info_conta(id, usuario, senha):
    print("[!]Id:",id)
    print("[!]usuario:",usuario)
    print("[!]senha:",senha)
    print("[!]quantidade de filmes favoritados:")
    input("\nPressione Enter para continuar...")

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
                favoritar_filme()
            case 2:
                pass
            case 3:
                info_conta(id, usuario, senha)
            case 4:
                pass
            case 5:
                pass
            case 6:
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

# Exibir os filmes favoritos
print("\nSeus filmes favoritos são:")
print(df_movies[df_movies['movieId'].isin(filmes_favoritos)][['movieId', 'title']])