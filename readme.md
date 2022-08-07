### Streamlit app with Neo4j

Application consits of three components
> Neo4j Server setup
> Graph Description
> Custom Query Editor

1. Neo4j Server setup
    Helps in connecting to remote Neo4j Server. Components 2 and 3 can be used only if the server connection is successful.
    Server config is passed between the components through session.
2. Graph Description
    Provides details related to labels, relationships, and schema available in the connected graph.
3. Custom Query Editor 
    Helps in writing custom cypher queries and execute the results
    
#### How to run the app locally
Step 1 : clone the repository
Step 2 : Create the python environment with environment.yml file in the folder
Step 3 : Activate the environment and from the root folder run `streamlit run apps/main.py config/inputs.yml`

Some of the source code is written but not currently being used. We will add functionality to the app as we progress in development

#### Work in progress
Adding visualizations and graphs