# add path to sys path
#%%

import sys
import os
from datetime import date, datetime as dt
import math


from numpy import tile
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

#import modules
import yaml
import streamlit as st
from apps_drivers import neo4j_driver
#Functions

def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.safe_load(file_descriptor)
    return data
    
    

# inp_data = yaml_loader('/Users/venkata.ponduri/Documents/streamlit_apps/config/inputs.yml')
# driver_obj = neo4j_driver.neo4j_class(inp_data)
# res = driver_obj.execute_query('MATCH (n:Order) return count(n) as count',True)
class app_streamlit:
    def __init__(self,inp_data=None):
        self.inp_data = inp_data
        self.queries = self.inp_data["neo4j_queries"]
        self.page_setup()
        self.hide_markdowns()
        self.sidebar_setup()
        
        if 'neo_server' not in st.session_state:
            st.session_state.neo_server = ''
        if 'port' not in st.session_state:
            st.session_state.port = ''
        if 'username' not in st.session_state:
            st.session_state.username = ''
        if 'password' not in st.session_state:
            st.session_state.password = ''
        if 'neo_status' not in st.session_state:
            st.session_state.neo_status = False     
    def page_setup(self):
        st.set_page_config(layout="wide")
    def title_setup(self,title='App'):
        st.header(title)
    def hide_markdowns(self):
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)        
    def get_query_names(self):
        return self.queries.keys()
    def get_neo4j_result(self,query):
        neo_driver = neo4j_driver.neo4j_class(self.inp_data)
        result = neo_driver.execute_query(query,True)
        return result
    def get_dataframe(self,key):
        print(key)
        query = self.queries[key]
        print('Here is the query',query)
        df = self.get_neo4j_result(query)
        return df
    def main(self):
        #tab1, tab2, tab3 = st.tabs(["Data Check", "Graph Stats", "Custome Query"])
        keys = self.get_query_names()
        num_keys = len(keys)
        target_columns = 3
        col_names = [list(keys)[i] for i in range(num_keys)]
        print(col_names)
        query_count = 0
        for j in range(0,num_keys,target_columns):
            cols_len = len(col_names[j:j+target_columns])
            [*cols]=st.columns(cols_len)
            for each_col in cols:
                with each_col:
                    st.write(list(keys)[query_count])
                    st.dataframe(self.get_dataframe(list(keys)[query_count]))
                    query_count+=1
    def neo4j_connection_setup(self):
        self.title_setup(title='Neo4j Server Connection')
        left,right =st.columns(2)
        form = left.form("template_form")
        st.session_state.neo_server = form.text_input("Neo4j URL",value='bolt://localhost:7687/')
        st.session_state.port = form.text_input("Neo4j Port",value='7687')
        st.session_state.username = form.text_input('User Name',value='neo4j')
        st.session_state.password = form.text_input('Password',type='password')
        submit = form.form_submit_button("Connect")
        neo_driver = neo4j_driver.neo4j_class(
            {'neo4j_server':{
                'server_uri':st.session_state.neo_server,
                'port':st.session_state.port,
                'username':st.session_state.username,
                'password':st.session_state.password
             }})
        if submit:
            neo_driver.check_connection()
        try:
            st.session_state.neo_status = neo_driver.check_connection()
        except Exception as e:
            st.session_state.neo_status = False
            
        if 'current_status' not in st.session_state:
            st.session_state.current_status = ''
        
        if(st.session_state.neo_status==True):
            st.session_state.current_status = '### Current Status : Connected'
        else:
            st.session_state.current_status = '### Current Status : Server Not Connected'
            
        form.write(st.session_state.current_status)    
    def graph_description(self):
        if (st.session_state.neo_status):
            st.write('### Active Neo4j Server ::: ',st.session_state.neo_server)
            neo_driver = neo4j_driver.neo4j_class(
            {'neo4j_server':{
                'server_uri':st.session_state.neo_server,
                'port':st.session_state.port,
                'username':st.session_state.username,
                'password':st.session_state.password
             }})
            st.write('')
            labels,relationships,constraints,test = st.columns(4)
            neo_labels = neo_driver.get_node_labels()
            labels.write('#### Existing Labels')
            labels.dataframe(neo_labels)
            
            neo_relations = neo_driver.get_relationship_labels()
            relationships.write('#### Existing Relationships')
            relationships.dataframe(neo_relations)
            
            neo_constraints = neo_driver.get_constraints()
            constraints.write('#### Existing Constraints')
            constraints.dataframe(neo_constraints)
            
        else:
            st.write(' ### Neo4j Server not connected. Please check the crendentials')   
    def sidebar_setup(self):
        self.option = st.sidebar.selectbox('Menu',['Neo4j Connection','Graph Description','Custom Query Editor'])
    def run_custom_cypher(self):
        st.write('Clicked')
    def custome_query(self):
        st.write('### Query Editor')
        if (st.session_state.neo_status):
            st.write('### Active Neo4j Server ::: ',st.session_state.neo_server)
            neo_driver = neo4j_driver.neo4j_class(
            {'neo4j_server':{
                'server_uri':st.session_state.neo_server,
                'port':st.session_state.port,
                'username':st.session_state.username,
                'password':st.session_state.password
             }})
            query = st.text_area(label='Enter Cypher Statement ')
            run_btn = st.button(label='RUN')
            if(run_btn):
                df=neo_driver.execute_query(query,True)
                st.dataframe(df)
            
        else:
            st.write(' ### Neo4j Server not connected. Please check the crendentials')
        
        
if __name__=="__main__":
    inp_data = yaml_loader(sys.argv[1])
    app = app_streamlit(inp_data=inp_data)
    if app.option=='Graph Description':
        app.graph_description()
        
    elif app.option =='Neo4j Connection':
        app.neo4j_connection_setup()
    else:
        app.custome_query()
    
