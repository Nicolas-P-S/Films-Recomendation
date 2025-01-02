<h1 align="center">🎬 FILMS RECOMMENDATION SYSTEM 🎬</h1>

<p align="center">
    Um sistema de recomendação de filmes interativo, que utiliza Machine Learning para sugerir filmes baseados nas preferências dos usuários.
</p>

---

## 📚 Sobre o Projeto

Este projeto oferece uma experiência personalizada de recomendação de filmes com funcionalidades como:

- **Sistema de Login e Registro**: Para salvar as preferências de filmes dos usuários.
- **Favoritar Filmes**: Pesquise, avalie e adicione seus filmes favoritos.
- **Recomendações Personalizadas**: Sugestões baseadas nos filmes favoritados, utilizando vetores TF-IDF e similaridade de cossenos.
- **Exploração de Filmes**: Pesquise filmes por nome, mesmo com pequenas diferenças ou erros de digitação.
- **Armazenamento Local**: Utiliza SQLite para gerenciar usuários e filmes favoritos.

---

## ⚙️ Funcionalidades

- **Favoritar Filmes**: Escolha filmes favoritos e adicione avaliações (1-5 estrelas).
- **Listar Favoritos**: Veja a lista de filmes salvos e suas avaliações.
- **Recomendações Inteligentes**: Baseadas em informações como gêneros e tags.
- **Informações da Conta**: Detalhes do usuário e quantidade de filmes favoritados.

## 🚀 Como Rodar o Projeto

### Pré-requisitos

1. **Python 3.9+**: Certifique-se de ter uma versão atualizada do [Python](https://www.python.org/downloads/).
2. **Bibliotecas Necessárias:** Instale as dependências usando o comando:
   ```bash
   pip install -r requirements.txt
   ```

### Executando o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/Nicolas-P-S/Films-Recomendation.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd films-recommendation
   ```
3. Execute o arquivo principal:
   ```bash
   python app.py
   ```

### Estrutura de Dados

- `ml-latest-small/`: Conjunto de dados de filmes (necessário para as recomendações).
- `login.db`: Banco de dados SQLite para usuários e filmes favoritos (gerado automaticamente).

## 🛠 Tecnologias Utilizadas

- **Python 3.9+**
- **SQLite** para armazenamento local.
- **scikit-learn** para cálculo de similaridade.
- **Pandas** para manipulação de dados.
- **TfidfVectorizer** para processamento de texto.

## 🌟 Funcionalidades Planejadas

- Implementar recomendação baseada em comportamento de outros usuários.
- Criar uma interface gráfica amigável.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.