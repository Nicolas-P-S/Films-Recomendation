import os

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

    print("Registro criado com sucesso!","\nusuario:", usuario,"\nsenha:", senha)
    input()
    os.system("cls")
    return usuario, senha

def menu():
    print("----------BEM VINDO ao bla bla bla----------")
    escolha=input("\nEscolha a opção:\nRegister-1\nLogin-2\n\nin: ")

    match int(escolha):
        case 1:
            os.system("cls")
            usuario, senha = register()
            return usuario, senha
        case 2:
            os.system("cls")
            print("l")
