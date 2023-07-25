import psycopg2
import pandas as pd
import warnings

class BD:
    def __init__(self):
        warnings.simplefilter("ignore")
    
    def abrirConexao(self):
        try:
            self.connection = psycopg2.connect(database = "db_diulliosantos",
                                    user="diulliosantos",        
                                    password="diulliosantosdatajourney",
                                    host = "azxpsg01.postgres.database.azure.com")
        
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao se conectar ao Banco de dados", error)
  
    def updateorinsertDados(self, date, rede_uf, uf, canal, recencia, frequencia, valor, score_frequencia, score_valor, score_recencia, score):
        try:
            # self.abrirConexao()
            cursor = self.connection.cursor()

            # Verificar se o registro já existe na tabela rfv.analysis
            postgres_check_query = """
            SELECT id FROM rfv.analysis WHERE rede_uf = %s AND canal = %s
            """
            cursor.execute(postgres_check_query, (rede_uf, canal))
            result = cursor.fetchone()

            if result:
                # Atualizar o registro existente na tabela rfv.analysis
                id = result[0]
                postgres_update_query = """
                UPDATE rfv.analysis 
                SET recencia = %s, frequencia = %s, valor = %s, score_frequencia = %s, score_valor = %s, score_recencia = %s, score = %s 
                WHERE id = %s
                """
                record_to_update = (recencia, frequencia, valor, score_frequencia, score_valor, score_recencia, score, id)
                cursor.execute(postgres_update_query, record_to_update)
            else:
                # Inserir um novo registro na tabela rfv.analysis
                postgres_insert_analysis = """
                INSERT INTO rfv.analysis (rede_uf, uf, canal, recencia, frequencia, valor, score_frequencia, score_valor, score_recencia, score) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                record_to_insert_analysis = (rede_uf, uf, canal, recencia, frequencia, valor, score_frequencia, score_valor, score_recencia, score)
                cursor.execute(postgres_insert_analysis, record_to_insert_analysis)

                # Obter o id do registro recém-inserido
                cursor.execute("SELECT currval('rfv.analysis_id_seq')")
                id = cursor.fetchone()[0]

            # Inserir na tabela rfv.evolucao
            postgres_insert_evolucao = """
            INSERT INTO rfv.evolucao (id_analysis, date, recencia, frequencia, valor, score_freq, score_valor, score_recencia, score) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            record_to_insert_evolucao = (id, date, recencia, frequencia, valor, score_frequencia, score_valor, score_recencia, score)
            cursor.execute(postgres_insert_evolucao, record_to_insert_evolucao)

            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Falha ao inserir registro na tabela", error)
        finally:
            if(self.connection):
                cursor.close()    
                # self.connection.close()

    def closeConexao(self):
        if(self.connection):
            self.connection.close()