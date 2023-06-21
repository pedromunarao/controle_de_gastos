from sqlite3 import Error
import conn_bd
from tabulate import tabulate
from colorama import Fore, Style
from termcolor import colored
from hashlib import sha256
from pwinput import pwinput


#CLASSE AUXILIAR!


class Auxiliar:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()
    

    def lista_id(self, info_id):
    #retorna lista de todos os ids de uma tabela
        try:
            self.cursor.execute(f"SELECT {info_id[0]} FROM {info_id[1]};")
            results = self.cursor.fetchall()
            lista_id = [row[0] for row in results]
            return lista_id
        #metodo: lista_id(("nome id", "nome tabela"))
        except Error as e:
            print(f"Erro retornar lista de ids: {e}")

    
    def enter(self):
        enter = colored('ENTER', 'red')
        input(f'Pressione {enter} para continuar!')

    
    def check_senha(self, id_user):
        try:
            self.cursor.execute(f"SELECT senha FROM usuarios WHERE idUsuarios = ?", id_user)
            r = self.cursor.fetchall()
            return r[0][0]
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao retornar senhas: {e}")


    def autenticacao(self):
        def senha_encode():
            senha = pwinput("Insira sua senha: ", "*")
            hash_senha = sha256(senha.encode())
            arm_senha = hash_senha.hexdigest()
            return arm_senha
        a = int(input("Insira o seu ID Usuário: "))
        k = Auxiliar.check_senha(self, (a, ))
        b = senha_encode()
        if k == b:
            return a, 1
        else:
            return a, 0 

    def sumdesp_cat(self):
        self.cursor.execute("SELECT SUM(t.valor), d.idCat FROM transacoes t INNER JOIN despesas d ON d.idDespesas = t.idDespesas GROUP BY d.idCat;")
        r = self.cursor.fetchall()
        return r
    

    def sumgan_cat(self):
        self.cursor.execute("SELECT SUM(t.valor), g.idCat FROM transacoes t INNER JOIN ganhos g ON g.idGanhos = t.idGanhos GROUP BY g.idCat;")
        r = self.cursor.fetchall()
        return r
#CLASSE CATEGORIAS!!


class Categorias:
    def __init__(self, conn):
        self.nome_cat = ""
        self.conn = conn
        self.cursor = self.conn.cursor()
        #inicializar variaveis


    def add_cat(self, nome_cat):
        try:
            self.cursor.execute(f"INSERT INTO categorias (nome) VALUES (?);", nome_cat)
            self.conn.commit()
            return "add_cat(('nome cat', ))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao adicionar categoria: {e}")


    def update_cat(self, info_cat):
        try:
            self.cursor.execute("UPDATE categorias SET nome = ? WHERE idCategorias = ?;", info_cat)
            self.conn.commit()
            return "update_cat(('nome a ser atualizado', 'id categoria'))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao atualizar categoria: {e}")


    def remove_cat(self, id_cat):
        try:
            self.cursor.execute("DELETE FROM categorias WHERE idCategorias = ?;", id_cat)
            self.conn.commit()
            return "remove_cat(('id categoria', ))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao remover categoria: {e}")


    def check_cat(self):
        try:
            self.cursor.execute("SELECT * FROM categorias;")
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'ID Categoria', 'Nome Categoria' + Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
            return r
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar categorias: {e}")

    def val_cat(self):
        try:
            self.cursor.execute("SELECT * FROM categorias;")
            r = self.cursor.fetchall()
            return r
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar categorias: {e}")
            

#CLASSE DESPESAS!!


class Despesas:
    def __init__(self, conn):
        self.nome_desp = ""
        self.id_cat = 0
        self.conn = conn
        self.cursor = self.conn.cursor()
        #inicializar variaveis
    

    def add_desp(self, info_desp):
        try:
            #verifica se a categoria existe
            aux = int(info_desp[1])
            info_id = ("idCategorias", "categorias")
            if aux in Auxiliar.lista_id(self, info_id):
                self.cursor.execute("INSERT INTO despesas (nome, idCat) VALUES (?, ?);", info_desp)
                self.conn.commit()
                return "add_desp(('nome despesa', 'id categoria'))"
            else:
                print(colored("Categoria inexistente", "red"))
                pass
        except Error as e:
            e = colored(e, "red")
            print(e)


    def update_desp(self, info_desp, cat_desp = 0):
        try:
            if cat_desp != 0: #update categoria despesa
                self.cursor.execute("UPDATE despesas SET idCat = ? WHERE idDespesas = ?", cat_desp)
                self.conn.commit()
                return "update_desp(0 ,('id categoria', 'id despesa'))" 
            else: #update nome despesa
                self.cursor.execute("UPDATE despesas SET nome = ? WHERE idDespesas = ?", info_desp)
                self.conn.commit()
            return "update_desp(('nome desp', 'id despesa'))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao atualizar despesa: {e}")


    def remove_desp(self, id_desp):
        try:
            self.cursor.execute("DELETE FROM despesas WHERE idDespesas = ?;", id_desp)
            self.conn.commit()
            return "remove_desp(('id despesa', ))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao remover despesa: {e}")


    def check_desp(self):
        try:
            self.cursor.execute("SELECT d.nome, d.idDespesas, d.idCat FROM despesas d ORDER BY d.idCat")
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'Nome Despesa', 'ID Despesa', 'ID Categoria' + Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
            return "check_desp()"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar despesas: {e}")


#CLASSE GANHOS!!


class Ganhos:
    def __init__(self, conn):
        self.nome_ganho = ""
        self.id_cat = 0
        self.conn = conn
        self.cursor = self.conn.cursor()
        #inicializar variaveis
    

    def add_ganho(self, info_ganho):
        try:
            #verifica se a categoria existe
            aux = int(info_ganho[1])
            info_id = ("idCategorias", "categorias")
            if aux in Auxiliar.lista_id(self, info_id):
                self.cursor.execute("INSERT INTO ganhos (nome, idCat) VALUES (?, ?);", info_ganho)
                self.conn.commit()
                return "add_ganho(('nome ganho', 'id categoria'))"
            else:
                print(colored("Categoria inexistente", "red"))
                pass
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao adicionar ganho: {e}")

    
    def update_ganho(self, info_ganho, op):
        try:
            if op == 1:
                aux = int(info_ganho[0])
                info_id = ("idCategorias", "categorias")
                if aux in Auxiliar.lista_id(self, info_id):
                #se desejar atualizar categoria do ganho
                    self.cursor.execute("UPDATE ganhos SET idCat = ? WHERE idGanhos = ?", info_ganho)
                    self.conn.commit()  
                else:  
                    print(colored("Categoria inexistente", "red"))
                    pass
                return "update_ganho(('id categoria', 'id ganho'), 1)"
            if op == 2: #se desejar atualizar nome da despesa
                self.cursor.execute("UPDATE ganhos SET nome = ? WHERE idGanhos = ?", info_ganho)
                self.conn.commit()
            return "update_ganho(('nome ganho', 'id ganho'), 2)"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao atualizar ganho: {e}")


    def remove_ganho(self, id_ganho):
        try:
            self.cursor.execute("DELETE FROM ganhos WHERE idGanhos = ?;", id_ganho)
            self.conn.commit()
            return "remove_ganho(('id ganho', ))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao remover ganho: {e}")


    def check_ganho(self):
        try:
            self.cursor.execute("SELECT * FROM ganhos ORDER BY idCat")
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'ID Ganho', 'Nome Ganho', "ID Categoria" + Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
            return "check_ganho()"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar ganhos: {e}")


#CLASSE USUARIOS!!


class Usuarios:
    def __init__(self, conn):
        self.nome_usr = ""
        self.__senha = ""
        self.nome = ""
        self.data_nasc = ""
        self.conn = conn
        self.cursor = self.conn.cursor()
        #inicializar variaveis

    def add_usr(self, info_usr):
        try:
            info_usr = list(info_usr)
            senha = str(info_usr[1])
            hash_senha = sha256(senha.encode())
            arm_senha = hash_senha.hexdigest()
            info_usr[1] = arm_senha
            self.cursor.execute(f"INSERT INTO usuarios (nome, senha, nomeComp, dataNasc) VALUES (?, ?, ?, ?);", info_usr)
            self.conn.commit()
            return "add_usr(('nome_usr, 'senha', 'nome compl', 'data nasc'))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao adicionar usuário: {e}")


    def update_usr(self, info_usr, op):
        try:
            if op == 1:
                self.cursor.execute("UPDATE usuarios SET nome = ? WHERE idUsuarios = ?;", info_usr)
                self.conn.commit()
            if op == 2:
                self.cursor.execute("UPDATE usuarios SET senha = ? WHERE idUsuarios = ?;", info_usr)
                self.conn.commit()
            if op == 3:
                self.cursor.execute("UPDATE usuarios SET nomeComp = ? WHERE idUsuarios = ?;", info_usr)
                self.conn.commit()
            if op == 4:
                self.cursor.execute("UPDATE usuarios SET dataNasc = ? WHERE idUsuarios = ?;", info_usr)
                self.conn.commit()
            return "update_usr(('info a ser update', 'id user'), num) 1=nome 2=senha 3=nomecompl 4=datanasc"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao atualizar informações de usuário: {e}")
    

    def remove_usr(self, info_usr):
        try:
            self.cursor.execute("DELETE FROM usuarios WHERE idUsuarios = ?", info_usr)
            self.conn.commit()
            return "remove_usr(('id user', ))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao excluir usuário: {e}")


    def check_usr(self):
        try:
            self.cursor.execute("SELECT * FROM usuarios;")
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'ID Usuario', 'Nome de Usuario', 'Senha', 'Nome Completo', 'Data de Nascimento' + Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
            return "check_usr()"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar usuários: {e}")
        

    def apresenta_id(self):
        try:
            self.cursor.execute("SELECT idUsuarios, nome FROM usuarios;")
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'ID Usuario', 'Nome de Usuario'+ Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
            return "apresenta_id()"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar usuários: {e}")


#CLASSE TRANSACOES!!


class Transacoes:
    def __init__(self, conn):
        self.valor = 0
        self.data = ""
        self.id_ganho = 0
        self.id_desp = 0
        self.conn = conn
        self.cursor = self.conn.cursor()
        #inicializar variaveis
    

    def add_trans(self, info_trans, op):
        try:
            if op == 1:
            #adicionar transacao tipo ganho
                aux = int(info_trans[2])
                aux2 = Auxiliar.lista_id(self, ("idGanhos", "ganhos"))
                if aux in aux2:
                #verificar se ganho existe
                    self.cursor.execute(f"INSERT INTO transacoes (valor, data, idGanhos, idDespesas, idUsuario) VALUES (?, ?, ?, ?, ?);", info_trans)
                    self.conn.commit()
                else:
                    print("Ganho inexistente!")
                return "add_trans(('valor', aux, 'idganho', 'iddesp', 'iduser'), op)"
            if op == 2:
            #adicionar transacao tipo desp
                aux = int(info_trans[3])
                aux2 = Auxiliar.lista_id(self, ("idDespesas", "despesas"))
                if aux in aux2:
                #verificar se desp existe
                    self.cursor.execute(f"INSERT INTO transacoes (valor, data, idGanhos, idDespesas, idUsuario) VALUES (?, ?, ?, ?, ?);", info_trans)
                    self.conn.commit()
                else:
                    print("Despesa inexistente!")
                return "add_trans(('valor', aux, 'idganho', 'iddesp', 'iduser'))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao adicionar transação: {e}")


    def update_trans(self, info_trans, op):
        try:
            if op == 1:
                self.cursor.execute("UPDATE transacoes SET valor = ? WHERE idTransacoes = ?;", info_trans)
                self.conn.commit()
            if op == 2:
                self.cursor.execute("UPDATE transacoes SET data = ? WHERE idTransacoes = ?;", info_trans)
                self.conn.commit()
            if op == 3:
                self.cursor.execute("UPDATE transacoes SET idDespesas = ? WHERE idTransacoes = ?;", info_trans)
                self.conn.commit()
            if op == 4:
                self.cursor.execute("UPDATE transacoes SET idGanhos = ? WHERE idTransacoes = ?;", info_trans)
                self.conn.commit()
            if op == 5:
                self.cursor.execute("UPDATE transacoes SET idUsuario = ? WHERE idTransacoes = ?;", info_trans)
                self.conn.commit()
            return "update_trans(('info a ser updated', ), op)"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao atualizar transação: {e}")


    def remove_trans(self, info_trans):
        try:
            self.cursor.execute("DELETE FROM transacoes WHERE idTransacoes = ?;", info_trans)
            self.conn.commit()
            return "remove_trans(('id trans', ))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao remover transação: {e}")


    def check_trans(self, op, iduser):
        try:
            if op == 1:
                self.cursor.execute("SELECT t.idTransacoes, t.valor, t.data, g.idGanhos, t.idUsuario FROM ganhos g INNER JOIN transacoes t ON t.idGanhos = g.idGanhos WHERE idUsuario = ?;", iduser)
                r = self.cursor.fetchall()
                headers=[Style.BRIGHT + Fore.WHITE + 'ID Transação', 'Valor Transação', 'Data Transação', 'ID Ganho', 'ID Usuário' + Fore.RESET + Style.NORMAL]
                print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
                return "check_trans()"
            if op == 2:
                self.cursor.execute("SELECT t.idTransacoes, t.valor, t.data, d.idDespesas, t.idUsuario FROM despesas d INNER JOIN transacoes t on t.idDespesas = d.idDespesas WHERE idUsuario =? ;", iduser)
                r = self.cursor.fetchall()
                headers=[Style.BRIGHT + Fore.WHITE + 'ID Transação', 'Valor Transação', 'Data Transação', 'ID Despesa', 'ID Usuário' + Fore.RESET + Style.NORMAL]
                print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
                return "check_trans()"
            if op == 3:
                self.cursor.execute("SELECT * FROM transacoes WHERE idUsuario = ?;", iduser)
                r = self.cursor.fetchall()
                headers=[Style.BRIGHT + Fore.WHITE + 'ID Transação', 'Valor Transação', 'Data Transação', 'ID Ganho', 'ID Despesa', 'ID Usuário' + Fore.RESET + Style.NORMAL]
                print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')                  
                return "check_trans()"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar transação: {e}")


#CLASSE CARTEIRA!!


class Carteiras:
    def __init__(self, conn):
        self.saldo = 0
        self.idUsr = 0
        self.conn = conn
        self.cursor = self.conn.cursor()
        #inicializar variaveis
    

    def add_carteira(self, info_cart):
        try:
            a = Auxiliar.lista_id(self, ("idUsuarios", "usuarios"))
            b = int(info_cart[1])
            if b in a:
                self.cursor.execute("INSERT INTO carteiras (saldo, idUsuario) VALUES (?,?);", info_cart)
                self.conn.commit()
            else:
                print("Usuário inexistente!")
            return "add_carteira(('saldo, iduser'))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao adicionar carteira: {e}")

    
    def update_carteira(self, info_cart):
        try:
            self.cursor.execute("UPDATE carteiras SET saldo = saldo + (?) WHERE idCarteiras = ?;", info_cart)
            self.conn.commit()
            return "update_carteira((saldo, 'id carte'))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao atualizar carteira: {e}")


    def remove_carteira(self, info_cart):
        try:
            self.cursor.execute("DELETE FROM carteiras WHERE idCarteiras = ?;", info_cart)
            self.conn.commit()
            return "remove_carteira(('id cart',))"
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao remover carteira: {e}")


    def check_carteira(self, info_cart):
        try:
            self.cursor.execute("SELECT c.idCarteiras, c.saldo FROM carteiras c INNER JOIN usuarios u ON c.idUsuario = ? WHERE c.idUsuario = u.idUsuarios;", info_cart)
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'ID Carteira', 'Saldo Atual' + Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}\n')
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar carteira: {e}")


    def saldo_da_carteira(self, info_cart):
        try:
            self.cursor.execute("SELECT sum(saldo) from carteiras WHERE idUsuario = ?;", info_cart)
            r = self.cursor.fetchall()
            headers=[Style.BRIGHT + Fore.WHITE + 'Saldo total atual' + Fore.RESET + Style.NORMAL]
            print(f'\n{tabulate(r, headers, tablefmt="heavy_outline", numalign="center", stralign="center")}')
        except Error as e:
            e = colored(e, "red")
            print(f"Erro ao checar carteira: {e}")