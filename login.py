import os
import sqlite3

def save_user(usuario, senha):
    conn = sqlite3.connect("login.db")
    cursor = conn.cursor()
    
    cursor.execute("create table if not exists user(id integer primary key autoincrement, name text not null, password text not null)")
    cursor.execute("insert into user (name, password) values (?, ?)", (usuario, senha)) #uso de placeholders(?) para evitar sql injection
    id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return id, usuario, senha

def search_user(usuario):
    try:
        conn = sqlite3.connect("login.db")
        cursor = conn.cursor()
        cursor.execute("select id, name, password from user where name = ?", (usuario,))
        retorno = cursor.fetchone()
        if retorno:
            return retorno  #tupla (id, usuario, senha)
        else:
            return None, None, None
    except sqlite3.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        return None, None, None



def register():
    usuario = ""
    senha = ""
    
    while len(usuario) <= 3 or len(usuario) >= 10:
        print("REGISTER\n")
        usuario=input("user: ")
        if len(usuario) <= 3 or len(usuario) >= 10:
            input("ERRO: usuario deve ter entre 3 e 10 caracteres!")
        os.system("cls")

    while len(senha) < 3 or len(senha) > 21:
        print("REGISTER\n")
        senha=input("password: ")
        if len(senha) < 3 or len(senha) > 21:
            input("ERRO: senha deve ter entre 4 e 20 caracteres!")
        os.system("cls")

    print("Usuario criado com sucesso!","\nusuario:", usuario,"\nsenha:", senha)
    input()
    return save_user(usuario, senha)

def login():
    if not os.path.exists("login.db"):
        input("ERRO: NÃO EXISTEM USUARIOS CADASTRADOS NA DATABASE!")
        return None, None, None
    
    while True:
        os.system("cls")
        print("Login\n")
        usuario = input("user: ")
        id, usuario_search, senha_search = search_user(usuario)

        if not usuario_search:
            input("Usuario invalido! Pressione Enter para tentar novamente.")
        else:
            break;

    while True:
        os.system("cls")
        print("Login\n")
        senha = input("password: ")
        if senha == senha_search:
            os.system("cls")
            print(f"Bem-vindo de volta, {usuario}!")
            return id, usuario, senha
        else:
            input("Senha incorreta! Pressione Enter para tentar novamente.")

def menu():
    os.system("cls")
    print("----------BEM VINDO ao bla bla bla----------")
    try:
        escolha = int(input("\nEscolha a opção:\nRegister-1\nLogin-2\n\nin: "))
    except ValueError:
        input("Entrada inválida! Pressione Enter para tentar novamente.")
        return menu()

    match escolha:
        case 1:
            os.system("cls")
            id, usuario, senha = register()
            if usuario is None or senha is None:
                return menu()
            else:
                return id, usuario, senha
        case 2:
            os.system("cls")
            id, usuario, senha = login()
            if usuario is None or senha is None:
                return menu()
            else:
                return id, usuario, senha
        case _:
            input("Opção inválida! Pressione Enter para tentar novamente.")
            return menu()