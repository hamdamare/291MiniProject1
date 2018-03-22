import sqlite3
import datetime
import time
import random

# Global variables
connection = None
cursor = None

 
# Print all the tasks a user can do
def loop():
    # Validate user input
    while(True):
        # Print the tasks 
        print(" "*5)
        print("SELECT ONE OF THE FOLLOWING TASKS OR ENTER 'Q' OR 'q' TO QUIT: ")
        print("---" * 20)
        print("1. BCNF Normalization and Decomposition")
        print("2. Attribute Closures")
        print("3. Equivalence of 2 Sets of Functional Dependencies")
        print()

        # Enter a decision
        decision = input("ENTER A NUMBER: ")
    
        # EXIT THE PROGRAM IF THE USER WANTS TO QUIT
        if(decision == "q" or decision=="Q"):
            exit(0)
        # GO TO BCNF FUNCTION
        elif(decision == "1"):
            bcnf()
        # GO TO CLOSOURE FUNCTION
        elif(decision == "2"):
            closure()

        # GO TO EQUIVALENCE FUNCTION
        elif(decision == "3"):
            equivalence()

    


# Print the table names in the database
def printTables():
    global connection, cursor
    cursor.execute('''
        select * from inputRelationSchemas;
    ''')
    connection.commit()

    nums = cursor.fetchall()


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------MAIN FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main function
def main():
    global connection, cursor

    filename= input("ENTER THE FILENAME OF THE DATABASE OR ENTER 'Q' OR 'q' TO QUIT: ")
    # EXIT THE PROGRAM IF THE USER WANTS TO QUIT
    if filename == "Q" or filename == 'q':
        exit(0)

    # Initialized the path to the database
    connection = sqlite3.connect("./" + filename)
    # Set the cusor to the cursor of the database
    cursor = connection.cursor()
    loop()
     
main()
    
