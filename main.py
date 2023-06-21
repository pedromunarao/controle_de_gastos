import tabelas as t, conn_bd as c
from datetime import datetime
from hashlib import sha256
from tabulate import tabulate
from termcolor import colored
from progress.bar import ChargingBar
from time import sleep
from colorama import Fore, Style
from pwinput import pwinput
import matplotlib.pyplot as plt

def limpar():
    # Importar o módulo os do sistema operacional
    import os
    # Importar um módulo par aguardar um tempo em segundos passados como parametro
    from time import sleep

    def screen_clear():
        #Linux ou Mac
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # Windows
            _ = os.system('cls')
    
    sleep(1)
    screen_clear()

if __name__ == '__main__':
    limpar()
    nome_banco = input(colored("Insira o nome do banco: ", 'green'))
    conn = c.criar_tabelas(nome_banco)

cat = t.Categorias(conn)
desp = t.Despesas(conn)
ganho = t.Ganhos(conn)
auxiliar = t.Auxiliar(conn)
user = t.Usuarios(conn)
trans = t.Transacoes(conn)
carteira = t.Carteiras(conn)


def adicionar_transacao(id_do_usuario):
    limpar()
    barra(0.02)
    limpar()
    headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
    menu = [[1, 'Ganhos'], [2, 'Despesas'], [3, 'Sair']]
    print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="center"))
    op = int(input("Digite a opção: "))
    if op == 1:
        limpar()
        ganho.check_ganho()
        idTransacao = input("Digite o ID do ganho: ")
        valor = float(input("Insira o valor da transação: "))
        data = datetime.now()
        limpar()
        barra(0.02)
        data_format = data.strftime("%d/%m/%Y %H:%M:%S")
        aux2 = (valor, data_format, idTransacao, None, id_do_usuario[0])
        trans.add_trans(aux2, op)
        limpar()
        barra(0.02)
        print(colored("Transação Adicionada", 'green'))
        barra(0.02)
        limpar()
        carteira.check_carteira((id_do_usuario[0], ))
        idCart = int(input("Insira o ID da carteira: "))
        limpar()
        carteira.update_carteira((valor, idCart))
        limpar()
        barra(0.02)
        print(colored("Ganho adicionado!", 'green'))
        limpar()
        adicionar_transacao(id_do_usuario)
    elif op == 2:
        limpar()
        desp.check_desp()
        idTransacao = input("Digite o ID da despesa: ")
        valor = float(input("Insira o valor da transação: "))
        data = datetime.now()
        limpar()
        data_format = data.strftime("%d/%m/%Y %H:%M:%S")
        aux2 = (valor, data_format, None, idTransacao, id_do_usuario[0])
        trans.add_trans(aux2, op)
        print(colored("Transação Adicionada", 'green'))
        limpar()
        carteira.check_carteira((id_do_usuario[0], ))
        idCart = int(input("Insira o ID da carteira: "))
        limpar()
        carteira.update_carteira((-valor, idCart))
        limpar()
        barra(0.02)
        print(colored("Despesa adicionada!", 'green'))
        limpar()
        adicionar_transacao(id_do_usuario)
    elif op == 3:
        limpar()
        barra(0.02)
        menu_principal(id_do_usuario)
    else:
        print(colored("Opção inválida!", "red"))

def adicionar_categoria(id_do_usuario):
    limpar()
    barra(0.02)
    limpar()
    category = input("Digite o nome da categoria: ")
    cat.add_cat((category, ))
    limpar()
    barra(0.02)
    print(colored("Categoria adicionada!", 'green'))
    limpar()
    cat.check_cat()
    auxiliar.enter()
    menu_principal(id_do_usuario)

def mais_opcoes(id_do_usuario):
    limpar()
    headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
    menu = [[1, 'Manter Categorias'], [2, 'Manter Despesas'], [3, 'Manter Ganhos'], [4, 'Manter Usuários'], [5, 'Manter Transações'], [6, 'Manter Carteiras'], [7, 'Sair']]
    print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
    op = int(input("Escolha sua opção: "))
    limpar()
    while op < 8:
        if op == 1:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Adicionar Categoria'], [2, 'Atualizar Categoria'], [3, 'Remover Categoria'], [4, 'Ver Categorias'], [5, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
            op3 = int(input("Escolha sua opção: "))
            limpar()
            while op3 < 6:
                if op3 == 1:
                    limpar()
                    nome_cat = input("Insira o nome da categoria: ")
                    cat.add_cat((nome_cat, ))
                    print(colored("Categoria adicionada com sucesso!", 'green'))
                    mais_opcoes(id_do_usuario)
                elif op3 == 2:
                    limpar()
                    cat.check_cat()
                    id_cat = int(input("Insira o id da categoria a ser atualizada: "))
                    nome_cat = input("Insira o nome da categoria: ")
                    cat.update_cat((nome_cat, id_cat))
                    mais_opcoes(id_do_usuario)
                elif op3 == 3:
                    limpar()
                    cat.check_cat()
                    id_cat = int(input("Insira o id da categoria a ser removida: "))
                    cat.remove_cat((id_cat, ))
                    print(colored("Categoria removida com sucesso!", 'green'))
                    mais_opcoes(id_do_usuario)
                elif op3 == 4:
                    limpar()
                    cat.check_cat()
                    auxiliar.enter()
                    mais_opcoes(id_do_usuario)
                elif op3 == 5:
                    limpar()
                    mais_opcoes(id_do_usuario)
            else:
                limpar
                print(colored("Opção inválida!", 'red'))
        elif op == 2:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Adicionar Despesa'], [2, 'Atualizar Despesa'], [3, 'Remover Despesa'], [4, 'Ver Despesas'], [5, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
            op3 = int(input("Escolha sua opção: "))
            while op3 < 6:
                if op3 == 1:
                    limpar()
                    nome_desp = input("Insira o nome da despesa: ")
                    cat.check_cat()
                    cat_desp = int(input("Insira a categoria da despesa: "))
                    limpar()
                    barra(0.02)
                    desp.add_desp((nome_desp, cat_desp))
                    print(colored("Despesa adicionada com sucesso!", 'green'))
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 2:
                    limpar()
                    headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
                    menu = [[1, 'Atualizar Categoria'], [2, 'Atualizar Nome']]
                    print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
                    sel = int(input("Escolha sua opção: "))
                    if sel == 1:
                        limpar()
                        desp.check_desp()
                        id_desp = int(input("Insira o id da despesa: "))
                        id_cat = int(input("Insira o novo id da categoria: "))
                        desp.update_desp(1, (id_cat, id_desp))
                        limpar()
                        barra(0.02)
                        print(colored("Categoria da despesa atualizada com sucesso!", 'green'))
                        barra(0.02)
                        mais_opcoes(id_do_usuario)
                    elif sel == 2:
                        limpar()
                        desp.check_desp()
                        id_desp = int(input("Insira o id da despesa: "))
                        nome_desp = input("Insira o novo nome da despesa: ")
                        desp.update_desp((nome_desp, id_desp))
                        limpar()
                        barra(0.02)
                        print(colored("Nome da despesa atualizado com sucesso!", 'green'))
                        barra(0.02)
                        mais_opcoes(id_do_usuario)
                    else:
                        print(colored("Opção inválida!", 'red'))
                        mais_opcoes(id_do_usuario)
                elif op3 == 3:
                    limpar()
                    desp.check_desp()
                    id_desp = int(input("Insira o id da despesa a ser removida: "))
                    desp.remove_desp((id_desp, ))
                    barra(0.02)
                    print(colored("Despesa removida com sucesso!", 'red'))
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 4:
                    limpar()
                    barra(0.02)
                    desp.check_desp()
                    auxiliar.enter()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 5:
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                else:
                   print(colored("Opção inválida!", 'red'))
        elif op == 3:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Adicionar Ganho'], [2, 'Atualizar Ganho'], [3, 'Remover Ganho'], [4, 'Ver Ganhos'], [5, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
            op3 = int(input("Escolha sua opção: "))
            while op3 < 6:
                if op3 == 1:
                    limpar()
                    nome_ganho = input("Insira o nome do ganho: ")
                    limpar()
                    cat.check_cat()
                    cat_ganho = int(input("Insira a categoria do ganho: "))
                    limpar()
                    ganho.add_ganho((nome_ganho, cat_ganho))
                    barra(0.02)
                    print(colored("Ganho adicionado com sucesso!", 'green'))
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 2:
                    limpar()
                    headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
                    menu = [[1, 'Atualizar Categoria'], [2, 'Atualizar Nome']]
                    print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
                    sel = int(input("Escolha sua opção: "))
                    if sel == 1:
                        barra(0.02)
                        limpar()
                        cat.check_cat()
                        cat_ganho = int(input("Insira a nova categoria: "))
                        barra(0.02)
                        limpar()
                        ganho.check_ganho()
                        id_ganho = int(input("Insira o id do ganho: "))
                        ganho.update_ganho((cat_ganho, id_ganho), 1)
                        barra(0.02)
                        limpar()
                        print(colored("Ganho atualizado com sucesso!", 'green'))
                        barra(0.02)
                        mais_opcoes(id_do_usuario)
                    elif sel == 2:
                        limpar()
                        nome_ganho = input("Insira o novo nome: ")
                        ganho.check_ganho()
                        id_ganho = int(input("Insira o id do ganho: "))
                        ganho.update_ganho((nome_ganho, id_ganho), 2)
                        limpar()
                        barra(0.02)
                        print(colored("Ganho atualizado com sucesso!", 'green'))
                        barra(0.02)
                        mais_opcoes(id_do_usuario)
                    else:
                        print(colored("Opção inválida!", 'red'))
                        mais_opcoes(id_do_usuario)
                elif op3 == 3:
                    limpar()
                    ganho.check_ganho()
                    id_ganho = int(input("Insira o id do ganho a ser removido: "))
                    ganho.remove_ganho((id_ganho, ))
                    limpar()
                    barra(0.02)
                    print(colored("Ganho removido com sucesso!", 'green'))
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 4:
                    limpar()
                    barra(0.02)
                    ganho.check_ganho()
                    auxiliar.enter()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 5:
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                else:
                   print(colored("Opção inválida!", 'red'))
        elif op == 4:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Adicionar Usuário'], [2, 'Atualizar Usuário'], [3, 'Remover Usuário'], [4, 'Ver Usuários'], [5, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
            op3 = int(input("Escolha sua opção: "))
            while op3 < 6:
                if op3 == 1:
                    limpar()
                    barra(0.02)
                    a = criar_usuario()
                    user.add_usr(a)
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 2:
                    limpar()
                    headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
                    menu = [[1, 'Atualizar Nome de Usuário'], [2, 'Atualizar Senha'], [3, 'Atualizar Nome'], [4, 'Atualizar Data de Nascimento'], [5, 'Sair']]
                    print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
                    sel = int(input("Insira sua opção: "))
                    if sel == 1:
                        nome_user = input("Insira o novo nome de usuário: ")
                        user.check_usr()
                        iddo_user = int(input("Insira o id do usuário: "))
                        user.update_usr((nome_user, iddo_user), 1)
                    elif sel == 2:
                        limpar()
                        barra(0.02)
                        user.check_usr()
                        b = auxiliar.autenticacao()
                        if b[1] == 1:
                            limpar()
                            senha = pwinput("Insira a nova senha: ", "*")
                            hash_senha = sha256(senha.encode())
                            arm_senha = hash_senha.hexdigest()
                            user.update_usr((arm_senha, b[0]), 2)
                            mais_opcoes(id_do_usuario)
                        else:
                            limpar()
                            barra(0.10)
                            print(colored("Senha incorreta", 'red'))
                            mais_opcoes(id_do_usuario)
                    elif sel == 3:
                        limpar()
                        barra(0.02)
                        nomeComp_user = input("Insira o novo nome: ")
                        user.update_usr((nomeComp_user, id_do_usuario), 3)
                    elif sel == 4:
                        limpar()
                        barra(0.02)
                        dataNasc_user = input("Insira a nova data de nascimento: ")
                        barra(0.02)
                        user.update_usr((dataNasc_user, id_do_usuario), 4)
                    elif sel == 5:
                        limpar()
                        barra(0.02)
                        mais_opcoes(id_do_usuario)
                    else:
                        limpar()
                        print(colored("Opção inválida!", 'red'))
                        barra(0.02)
                        mais_opcoes(id_do_usuario)
                elif op3 == 3:
                    limpar()
                    barra(0.02)
                    user.check_usr()
                    id_user = int(input("Insira o id do usuário a ser removido: "))
                    barra(0.02)
                    user.remove_usr((id_user, ))
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 4:
                    limpar()
                    barra(0.02)
                    user.check_usr()
                    auxiliar.enter()
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 5:
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                else:
                   print(colored("Opção inválida!", 'red'))
                   barra(0.02)
                   mais_opcoes(id_do_usuario)
        elif op == 5:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Adicionar Transação'], [2, 'Atualizar Transação'], [3, 'Remover Transação'], [4, 'Ver Transações'], [5, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
            op3 = int(input("Escolha sua opção: "))
            while op3 < 6:
                if op3 == 1:
                    limpar()
                    barra(0.02)
                    adicionar_transacao(id_do_usuario)
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 2:
                    barra(0.02)
                    atualizar_trans(id_do_usuario)
                elif op3 == 3:
                    limpar()
                    trans.check_trans(3)
                    idtran = int(input("Insira o id da transação a ser removida: "))
                    limpar()
                    barra(0.02)
                    trans.remove_trans((idtran, ))
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 4:
                    limpar()
                    barra(0.02)
                    trans.check_trans(3, id_do_usuario)
                    auxiliar.enter()
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 5:
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                else:
                    print(colored("Opção inválida!", 'red'))
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
        elif op == 6:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Adicionar Carteira'], [2, 'Atualizar Carteira'], [3, 'Remover Carteira'], [4, 'Ver Carteiras'], [5, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
            op3 = int(input("Escolha sua opção: "))
            limpar()
            barra(0.02)
            while op3 < 6:
                if op3 == 1:
                    limpar()
                    user.check_usr()
                    idus = int(input("Insira o id do usuário para adicionar carteira: "))
                    carteira.add_carteira((0, idus))
                    limpar()
                    barra(0.02)
                    print(colored("Carteira adicionada!", 'green'))
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 2:
                    limpar()
                    user.check_usr()
                    idus = int(input("Insira o id do usuário: "))
                    limpar()
                    carteira.check_carteira((idus, ))
                    idcart = int(input("Insira o id da carteira: "))
                    val = float(input("Insira o valor a ser adicionado na carteira: "))
                    carteira.update_carteira((val, idcart))
                    limpar()
                    barra(0.02)
                    print(colored("Carteira atualizada!", 'green'))
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 3:
                    limpar()
                    user.check_usr()
                    idus = int(input("Insira o id do usuário para remover carteira: "))
                    limpar()
                    carteira.check_carteira((idus, ))
                    idcart = int(input("Insira o id da carteira a ser removida: "))
                    carteira.remove_carteira((idcart, ))
                    limpar()
                    barra()
                    print(colored("Carteira removida!", 'green'))
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 4:
                    limpar()
                    user.check_usr()
                    idus = int(input("Insira o id do usuário para ver carteiras: "))
                    limpar()
                    barra(0.02)
                    carteira.check_carteira((idus, ))
                    auxiliar.enter()
                    limpar()
                    barra(0.02)
                    mais_opcoes(id_do_usuario)
                elif op3 == 5:
                    limpar()
                    mais_opcoes(id_do_usuario)
            else:
                limpar()
                print(colored("Opção inválida!", 'red'))
        elif op == 7:
            limpar()
            menu_principal(id_do_usuario)
        else:
            limpar()
            print(colored("Opção inválida!", 'red'))

def atualizar_trans(id_do_usuario):
    limpar()
    headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
    menu = [[1, 'Atualizar Valor'], [2, 'Atualizar Data'], [3, 'Atualizar idDespesa'], [4, 'Atualizar idGanho'], [5, 'Atualizar idUsuario'], [6, 'Sair']]
    print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="left"))
    sel1 = int(input("Insira sua opção: "))
    limpar()
    barra(0.02)
    if sel1 == 1:
        limpar()
        trans.check_trans(3)
        idtran = int(input("Insira o id da transação: "))
        limpar()
        infotran = input("Insira o valor a ser atualizado: ")
        trans.update_trans((infotran, idtran), 1)
        limpar()
        barra(0.02)
        print(colored("Transação atualizada com sucesso!", 'green'))
    elif sel1 == 2:
        limpar()
        trans.check_trans(3)
        idtran = int(input("Insira o id da transação: "))
        limpar()
        infotran = input("Insira o data a ser atualizada: ")
        trans.update_trans((infotran, idtran), 2)
        limpar()
        barra(0.02)
        print(colored("Transação atualizada com sucesso!", 'green'))
    elif sel1 == 3:
        limpar()
        trans.check_trans(3)
        idtran = int(input("Insira o id da transação: "))
        limpar()
        infotran = input("Insira o id da despesa a ser atualizada: ")
        trans.update_trans((infotran, idtran), 3)
        limpar()
        barra(0.02)
        print(colored("Transação atualizada com sucesso!", 'green'))
    elif sel1 == 4:
        limpar()
        trans.check_trans(3)
        idtran = int(input("Insira o id da transação: "))
        limpar()
        infotran = input("Insira o id do ganho a ser atualizado: ")
        trans.update_trans((infotran, idtran), 4)
        limpar()
        barra(0.02)
        print(colored("Transação atualizada com sucesso!", 'green'))
    elif sel1 == 5:
        limpar()
        trans.check_trans(3)
        idtran = int(input("Insira o id da transação: "))
        limpar()
        infotran = input("Insira o id do usuario a ser atualizado: ")
        trans.update_trans((infotran, idtran), 5)
        limpar()
        barra(0.02)
        print(colored("Transação atualizada com sucesso!", 'green'))
    elif sel1 == 6:
        limpar()
        mais_opcoes(id_do_usuario)
    else:
        limpar()
        print(colored("Opção inválida!", 'red'))
        mais_opcoes(id_do_usuario)

def barra(tempo):
    bar = ChargingBar('Carregando...', max=20)
    for i in range(20):
        sleep(tempo)
        bar.next()
    bar.finish()

def barra2(tempo):
    bar = ChargingBar(colored('Reiniciando...', 'red', max=20))
    for i in range(20):
        sleep(tempo)
        bar.next()
    bar.finish()

def tela_login(): 
    try:
        limpar()
        headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu de login' + Fore.RESET + Style.NORMAL]
        menu = [[1, 'Fazer Login'], [2, 'Criar Usuário']]
        print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="center"))
        a = colored("opção", "white")
        esc = int(input(f"Insira sua {a}: "))
        limpar()
        if esc == 1:
            user.apresenta_id()
            b = auxiliar.autenticacao()
            if b[1] == 1:
                limpar()
                print(colored("Senha correta", 'green'))
                barra(0.02)
                limpar()
                return b
            else:
                limpar()
                print(colored("Senha incorreta", 'red'))
                barra(0.02)
                limpar()
                tela_login()
        elif esc == 2:
            info_user = criar_usuario()
            barra(0.02)
            limpar()
            print(colored("Usuário cadastrado com sucesso", 'green'))
            user.add_usr(info_user)
            limpar()
            id_do_usuario = tela_login()
            menu_principal(id_do_usuario[0])
        else:
            print(colored("Opção inválida", 'red'))
            tela_login()
    except:
        print(colored("Opcão inválida", "red"))
        limpar()
        print("Reiniciando...")
        tela_login()

def criar_usuario():
            nome_de_Usuario = input("Informe o nome de usuário: ")
            senha = input("Informe a senha: ")
            NomeComp = input("Informe o nome completo: ")
            DataNasc = input("Informe a data de nascimento (dd/mm/aaaa): ")
            return (nome_de_Usuario, senha, NomeComp, DataNasc)

def grafico_desp_cat():
    valor_por_cat_despesa = auxiliar.sumdesp_cat()
    cat_por_nome = cat.val_cat()
    cat_com_desp = []
    id_categorias = []
    valores = []
    i = 0
    for elem in valor_por_cat_despesa:
        cat_com_desp.append(valor_por_cat_despesa[i][1])
        i += 1 
    i = 0
    for elem in cat_por_nome:
        id_categorias.append(cat_por_nome[i][0])
        i += 1
    i = 0
    for elem in valor_por_cat_despesa:
        valores.append(valor_por_cat_despesa[i][0])
        i += 1 
    desp_nome = []
    for i in range(len(cat_com_desp)):
        if cat_com_desp[i] in id_categorias:
            j = cat_com_desp[i]
            pos = id_categorias.index(j)
            desp_nome.append(cat_por_nome[pos][1])
   
    labels = desp_nome
    vals = valores
    fig, ax = plt.subplots(figsize=(12,5))
    ax.pie(vals, labels=labels, autopct="%.1f%%", shadow=True)
    ax.set_title("Despesas por categoria", fontsize=16)
    plt.show()

def grafico_ganho_cat():
    valor_por_cat_despesa = auxiliar.sumgan_cat()
    cat_por_nome = cat.val_cat()
    cat_com_desp = []
    id_categorias = []
    valores = []
    i = 0
    for elem in valor_por_cat_despesa:
        cat_com_desp.append(valor_por_cat_despesa[i][1])
        i += 1 
    i = 0
    for elem in cat_por_nome:
        id_categorias.append(cat_por_nome[i][0])
        i += 1
    i = 0
    for elem in valor_por_cat_despesa:
        valores.append(valor_por_cat_despesa[i][0])
        i += 1 
    desp_nome = []
    for i in range(len(cat_com_desp)):
        if cat_com_desp[i] in id_categorias:
            j = cat_com_desp[i]
            pos = id_categorias.index(j)
            desp_nome.append(cat_por_nome[pos][1])


    labels = desp_nome
    vals = valores
    fig, ax = plt.subplots(figsize=(12,5))
    ax.pie(vals, labels=labels, autopct="%.1f%%", shadow=True)
    ax.set_title("Ganhos por categoria", fontsize=16)
    plt.show()

def menu_principal(id_do_usuario):
    try:
        limpar()
        id_do_usuario = str(id_do_usuario)
        carteira.saldo_da_carteira(id_do_usuario)
        headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
        menu = [[1, 'Adicionar Transação'], [2, 'Adicionar Categoria'], [3, 'Criar Carteira'], [4, 'Mais Opções'], [5, 'Gráfico'],[6, 'Sair']]
        print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="center"))
        a = colored("opção", "white")
        esc = int(input(f"Insira sua {a}: "))
        limpar()
        if esc == 1:
            adicionar_transacao(id_do_usuario)
        elif esc == 2:
            adicionar_categoria(id_do_usuario)
        elif esc == 3:
            carteira.add_carteira((0, id_do_usuario))
            limpar()
            barra(0.02)
            print(colored("Carteira adicionada", 'green'))
            limpar()
            barra(0.02)
            menu_principal(id_do_usuario)
        elif esc == 4:
            barra(0.02)
            mais_opcoes(id_do_usuario)
        elif esc == 5:
            headers = [Style.NORMAL + Fore.WHITE + 'Opção', 'Menu' + Fore.RESET + Style.NORMAL]
            menu = [[1, 'Gráfico ganho por categoria'], [2, 'Gráfico despesa por categoria'], [3, 'Sair']]
            print(tabulate(menu, headers, tablefmt="heavy_outline", numalign="center", stralign="center"))
            ta_gravando= int(input("Escolha sua opção: "))
            if ta_gravando == 1:
                grafico_ganho_cat()
            elif ta_gravando == 2:
                grafico_desp_cat()
            else:
                menu_principal(id_do_usuario)
        elif esc == 6:
            id_do_usuario = tela_login()
            menu_principal(id_do_usuario[0])
    except:
        print(colored("Erro", "red"))
        limpar()
        barra2(0.10)
        menu_principal(id_do_usuario)

id_do_usuario = tela_login()
menu_principal(id_do_usuario[0])