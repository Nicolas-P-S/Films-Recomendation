import pandas as pd
from difflib import get_close_matches
import login

# Carregar os dados
df_links = pd.read_csv("ml-latest-small/links.csv")
df_movies = pd.read_csv("ml-latest-small/movies.csv")
df_ratings = pd.read_csv("ml-latest-small/ratings.csv")
df_tags = pd.read_csv("ml-latest-small/tags.csv")

usuario, senha=login.menu()

# Criar um usuário
usuarios = []

usuarios.append({"usuario": usuario, "senha": senha})

# Função para pesquisar filmes
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
    return resultados_substring

# Selecionar filmes favoritos
print("\nPesquise e escolha seus filmes favoritos!")
filmes_favoritos = []

while True:
    nome_filme = input("\nDigite o nome do filme para pesquisar (ou 'sair' para finalizar): ")
    if nome_filme.lower() == "sair":
        break
    
    # Buscar filmes no dataframe
    resultados = pesquisar_filmes(nome_filme)
    
    if not resultados.empty:
        print("\nFilmes encontrados:")
        print(resultados[['movieId', 'title']])
        
        escolha = input("\nDigite o ID do filme para adicioná-lo aos favoritos (ou 'nenhum' para pular): ")
        if escolha.isdigit() and int(escolha) in resultados['movieId'].values:
            filmes_favoritos.append(int(escolha))
            print("Filme adicionado aos favoritos!")
        else:
            print("ID inválido ou nenhum filme selecionado.")
    else:
        print("Nenhum filme encontrado com esse nome ou similaridade.")

# Exibir os filmes favoritos
print("\nSeus filmes favoritos são:")
print(df_movies[df_movies['movieId'].isin(filmes_favoritos)][['movieId', 'title']])
