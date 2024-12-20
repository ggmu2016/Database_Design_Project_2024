# Database_Design_Project_2024

# Implemented Research Paper
Relational Query Synthesis & Decision Tree Learning
A paper that details a method to synthesize a query given output examples of an executed query.
https://www.seas.upenn.edu/~asnaik/assets/papers/vldb24_libra.pdf

# Software Setup Steps
1. Run command "pip install sqlalchemy" to install Flask-SQLAlchemy  
2. Run command "pip install psycopg2-binary" to install necessary dependencies  
Consult https://docs.sqlalchemy.org/en/20/tutorial/index.html for more information on SQL Alchemy

OR run "pip install -r requirements.txt" to install all necessary dependencies at once

# Software Running
1. Run command "python3 libra.py" to run the main algorithm  
2. Run command "python3 libra_queries_test.py" to run the testing unit

# Datasets 
Datasets are hosted on Neon.tech.
Here are the links to the spreadsheet representations of our datasets. These contain the data entries that are currently held in the DBMS.  
School dataset (used in libra.py): https://docs.google.com/spreadsheets/d/1yVK-vh60DtnToN40fMMd3KIGLydSTTsiD2wg6_uiH_A/edit?usp=sharing  
Football dataset (used in libra_test.py): https://docs.google.com/spreadsheets/d/1yAuEob48OQH7C4s1aX_cnSOoHMT0h2lpWTs8yz97NrY/edit?usp=sharing  
If direct access to the Neon interface is needed, please make an account at neon.tech and contact hxk210048@utdallas.edu for more information.  

# Files and Their Descriptions
* create_graph.py - Contains code to generate the query runtime graph
* create_large_dataset.py - Contains the schema definition of the larger data set used to test our system  
* create_tables.py - Contains the schema definition of the data set used to develop and run the system. The main algorithm uses this dataset  
* decision_tree_learning.py - Contains the logic, math, and functions to perform decision tree learning  
* libra_queries_test - Tests the 10 queries on the larger dataset
* libra.py - Contains the main algorithm. This script attempts to replicate the query: SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" < 500 AND department."school" = "Engineering"  
* queries.py - Contains 10 queries for large dataset ranked for complexity and helper functions
* query_to_table.py - Contains a helper to convert SQLAlchemy results to a python dictionary  
