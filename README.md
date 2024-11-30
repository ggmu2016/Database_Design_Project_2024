# Database_Design_Project_2024

# Implemented Research Paper
Relational Query Synthesis & Decision Tree Learning
A paper that details a method to synthesize a query given output examples of an executed query.
https://www.seas.upenn.edu/~asnaik/assets/papers/vldb24_libra.pdf

# Software Setup Steps
1. Run command "pip install sqlalchemy" to install Flask-SQLAlchemy  
2. Run command "pip install psycopg2-binary" to install necessary dependencies  
Consult https://docs.sqlalchemy.org/en/20/tutorial/index.html for more information on SQL ALchemy

# Software Running
1. Run command "python3 libra.py" to run the main algorithm  
2. Run command "python3 libra_test.py" to run the testing unit  

# Files and Their Descriptions
create_large_dataset.py - Contains the schema definition of the larger data set used to test our system  
create_tables.py - Contains the schema definition of the data set used to develop and run the system. The main algorithm uses this dataset  
decision_tree_learning.py - Contains the logic, math, and functions to perform decision tree learning  
libra_test.py - Contains the tests for multiple queries and compares the results  
libra.py - Contains the main algorithm. This script attempts to replicate the query: SELECT registration."studentID" FROM registration JOIN department ON registration."deptCode" = department."deptCode" WHERE registration."courseID" < 500 AND department."school" = "Engineering"  
query_to_table.py - Contains a helper to convert SQLAlchemy results to a python dictionary  
