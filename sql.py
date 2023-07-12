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
            # self.connection = psycopg2.connect(database = "postgres",
            #                         user="postgres",        
            #                         password="0903",
            #                         host = "localhost")
        
        except (Exception, psycopg2.Error) as error:
            if(self.connection):
                print("Falha ao se conectar ao Banco de dados", error)
  
    def inserirDados(self, ):
        try:
            self.abrirConexao()
            cursor = self.connection.cursor()
            postgres_insert_query = """INSERT INTO public.ifa (cd_ifa, nome, fabricante, dmf, ano, risco, chk_lhasa, chk_td50, chk_ttc, chk_ai, chk_readacross, chk_alertamercado, chk_predicao, chk_purga, chk_nitrosado, chk_testconf, chk_ames, chk_teorico) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            record_to_insert = (cd_ifa, nome, fabricante, dmf, ano, risco, chk_lhasa, chk_td50, chk_ttc, chk_ai, chk_readacross, chk_alertamercado, chk_predicao, chk_purga, chk_nitrosado, chk_testconf, chk_ames, chk_teorico)
            cursor.execute(postgres_insert_query, record_to_insert)

            sql_select = f"""
            SELECT * FROM public.ifa 
            order by id_ifa_pk desc 
            LIMIT 1
            """
            cursor.execute(sql_select)
            id_ifa_pfk = cursor.fetchone()[0]
            
        #insert racional
            postgres_insert_rac = """INSERT INTO public.racional_ifa (id_ifa_pfk, racional_ifa) VALUES (%s, %s)"""
            record_to_insert_rac = (id_ifa_pfk , racional_ifa)
            cursor.execute(postgres_insert_rac, record_to_insert_rac)
            self.connection.commit()
        except (Exception, psycopg2.Error) as error :
            if(self.connection):
                print("Falha ao inserir registro na tabela", error)
        finally:
            #closing database connection.
            if(self.connection):
                cursor.close()    
                self.connection.close()           
