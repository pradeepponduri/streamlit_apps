from neo4j import GraphDatabase
from functools import wraps
import pandas as pd

class neo4j_class:
    def __init__(self,config):
        try:
            neo_details = config['neo4j_server']
            self.server=neo_details['server_uri']
            self.user = neo_details['username']
            self.password = neo_details['password']           
        except Exception as e :
            print("Database connection error {0}".format(e))
    def check_connection(self):
        #print(self.server,'----',self.password,'---',self.user)
        status = False
        try:
            driver = self.open_neo4j_connection()
            connectivity = driver.verify_connectivity()
            status = True
            driver.close()
        except Exception as e:
            status = False
        return status
    def get_node_labels(self):
        label_type_query = """CALL db.labels()"""
        result = self.execute_query(label_type_query,True)
        return result
    def get_relationship_labels(self):
        reltn_type_query = """CALL db.relationshipTypes()"""
        result = self.execute_query(reltn_type_query,True)
        return result
        
    def get_constraints(self):
        reltn_type_query = """CALL db.constraints()"""
        result = self.execute_query(reltn_type_query,True)
        return result
    def open_neo4j_connection(self):
        try:
            driver = GraphDatabase.driver(self.server, auth=(self.user, self.password),encrypted=False)
            #print(f"\n Established the connection with {self.server}")
            return driver
        except Exception as e:
            print("Failed to Intiate Drive Check for logs in logs/neo4j.log ")
            print("Driver not intiated due to Error {0} \n".format(e))
        
    def execute_query(self,query, query_result=False):
        try:
            driver = self.open_neo4j_connection()
            with driver.session() as session:
                #print('Running Query : ',query)
                query_result = session.run(query)   
                
                if query_result:
                    #print([r.values() for r in query_result])
                    df = pd.DataFrame([r.values() for r in query_result], columns=query_result.keys())
                    return df
            if query_result:
                return df
        except :
            pass
        try:
            driver = self.open_neo4j_connection()
            with driver.session() as session:
                query_result = session.run(query)     
                if query_result:
                    df = pd.DataFrame([r.values() for r in query_result], columns=query_result.keys())
            session.close()
            if query_result:
                return df
        except Exception as e:
            print("Error check for logs in neo4j_driver.log")
            raise Exception(e)