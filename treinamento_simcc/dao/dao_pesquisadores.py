import pandas as pd
from pprint import pprint
from dao.banco import Connection  # Caso o arquivo de conexão seja 'connection.py' (ou 'dao.banco' se for 'banco.py')
from model.pesquisador import Pesquisador


# 1. READ (Consultar)
def consultar_pesquisadores():
    script_sql = """
        SELECT
            pesquisadores_id, 
            lattes_id, 
            nome
        FROM 
            pesquisadores;
        """

    with Connection() as conn:
        registro = conn.select(script_sql)

    # Exibe o registro retornado do banco
    pprint(registro)

    df = pd.DataFrame(registro)
    
    # Ajusta os nomes das colunas se necessário
    if not df.empty and len(df.columns) == 3:
        df.columns = ["pesquisadores_id", "lattes_id", "nome"]

    lista_de_pesquisadores = list()
    for index, dados in df.iterrows():
        print(dados)
        pesquisador = Pesquisador()
        pesquisador.pesquisadores_id = dados["pesquisadores_id"]
        pesquisador.lattes_id = dados["lattes_id"]
        pesquisador.nome = dados["nome"]

        lista_de_pesquisadores.append(pesquisador.gerar_json())

    return lista_de_pesquisadores


# 2. CREATE (Inserir)
def criar_pesquisador(pesquisadores_id, lattes_id, nome):
    script_sql = """
        INSERT INTO pesquisadores (
            pesquisadores_id, 
            lattes_id, 
            nome
        ) VALUES (
            %s, %s, %s
        );
    """
    with Connection() as conn:
        conn.exec(script_sql, [pesquisadores_id, lattes_id, nome])


# 3. UPDATE (Atualizar)
def atualizar_pesquisador(pesquisadores_id, lattes_id, nome):
    script_sql = """
        UPDATE pesquisadores
        SET 
            lattes_id = %s, 
            nome = %s
        WHERE 
            pesquisadores_id = %s;
    """
    with Connection() as conn:
        conn.exec(script_sql, [lattes_id, nome, pesquisadores_id])


# 4. DELETE (Apagar)
def apagar_pesquisador(pesquisadores_id):
    script_sql = """
        DELETE FROM 
            pesquisadores
        WHERE 
            pesquisadores_id = %s;
    """
    with Connection() as conn:
        conn.exec(script_sql, [pesquisadores_id])