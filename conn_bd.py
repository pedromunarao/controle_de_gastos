import sqlite3
from sqlite3 import Error
from termcolor import colored

#criar as tabelas do banco e verificar erros
def criar_tabelas(nome_banco):
    conn = sqlite3.connect(nome_banco)
    c = conn.cursor()
    try: 
        #criar tabela categorias
        c.execute("""CREATE TABLE IF NOT EXISTS "categorias" ("idCategorias"	INTEGER NOT NULL,"nome"	TEXT NOT NULL,PRIMARY KEY("idCategorias" AUTOINCREMENT))""")
        #criar tabela despesas
        c.execute("""CREATE TABLE IF NOT EXISTS "despesas" ("idDespesas"	INTEGER NOT NULL,"nome"	TEXT,"idCat"INTEGER,PRIMARY KEY("idDespesas" AUTOINCREMENT))""")
        print(colored("Tabelas criadas com sucesso!", 'green'))
        #criar tabela ganhos
        c.execute("""CREATE TABLE IF NOT EXISTS "ganhos" ("idGanhos"	INTEGER NOT NULL,"nome"	TEXT,"idCat"	INTEGER NOT NULL,PRIMARY KEY("idGanhos" AUTOINCREMENT),FOREIGN KEY("idCat") REFERENCES "categorias"("idCategoria"))""")
        #criar tabela transacoes
        c.execute("""CREATE TABLE IF NOT EXISTS "transacoes" ("idTransacoes"	INTEGER NOT NULL, "valor"	REAL NOT NULL, "data"	DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "idGanhos"	INTEGER, "idDespesas"	INTEGER, "idUsuario"	INTEGER, PRIMARY KEY("idTransacoes" AUTOINCREMENT), FOREIGN KEY("idGanhos") REFERENCES "ganhos"("idGanhos"), FOREIGN KEY("idUsuario") REFERENCES "usuarios"("idUsuario"))""")
        #criar tabela usuarios
        c.execute("""CREATE TABLE IF NOT EXISTS "usuarios" ("idUsuarios"	INTEGER NOT NULL,"nome"	TEXT NOT NULL,"senha"	TEXT NOT NULL,"nomeComp"	TEXT,"dataNasc"	TEXT NOT NULL,PRIMARY KEY("idUsuarios" AUTOINCREMENT))""")
        #criar tabela carteiras
        c.execute("""CREATE TABLE IF NOT EXISTS "carteiras" ("idCarteiras"	INTEGER NOT NULL,"saldo"	REAL NOT NULL,"idUsuario"	INTEGER NOT NULL,PRIMARY KEY("idCarteiras"),FOREIGN KEY("idUsuario") REFERENCES "usuarios")""")
        return conn    
    except Error as e:
        e = colored(e, "red")
        print(f"{e}")