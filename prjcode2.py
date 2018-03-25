import sqlite3
import datetime
import time
import random

# CITATIONS: 
# https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list 
# https://stackoverflow.com/questions/8866652/determine-if-2-lists-have-the-same-elements-regardless-of-order


# Global variables
connection = None
cursor = None


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------logout FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Terminate the program
def logout():
    exit(0)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------EQUIVALENCE FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Equivalence of 2 Sets of Functional Dependencies
def equivalence():
    global connection, cursor

    # GET THE NAMES OF EACH TABLE
    cursor.execute('''
        select * from inputRelationSchemas; ''')
    connection.commit()
    nums = cursor.fetchall()
    names = []
    for num in nums:
        names.append(num[0])


    print("\n"*60)
    print("Equivalence of 2 Sets of Functional Dependencies ")
    print("---" * 50)
    print()

    f1_names = []
    f2_names = []

    # GET F1 NAMES
    print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS F1")
    print("---" * 50)
    # PRINT THE TABLES
    printTables()
    # VALIDATE CHOICES
    while True:
        choice = input("ENTER NAME OR ENTER 'D' or 'd' WHEN DONE: ")
        if (choice == "d" or choice == "D"):
            break
        elif (choice in names and choice not in f1_names):
            f1_names.append(choice)
        else:
            print("TRY AGAIN,", end=" ")


    # GET F2 NAMES
    print("\n"*5)
    print("---" * 50)
    print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS F2")
    print("---" * 50)
    # PRINT THE TABLES
    printTables()
    # VALIDATE CHOICES
    while True:
        choice = input("ENTER NAME OR ENTER 'D' or 'd' WHEN DONE: ")
        if (choice == "d" or choice == "D"):
            break
        elif (choice in names and choice not in f2_names):
            f2_names.append(choice)
        else:
            print("TRY AGAIN,", end=" ")

    fd1 = []
    fd2 = []

    # GET THE FDs FOR F1
    for name in f1_names:
        cursor.execute('''
        select FDs 
        from InputRelationSchemas
        where Name = ?''', (name,))
        nums = cursor.fetchone()
        list_nums= nums[0].split(";")
        for i in list_nums:
            fd1.append(i)
    
    # GET THE FDs FOR F2
    for name in f2_names:
        cursor.execute('''
        select FDs 
        from InputRelationSchemas
        where Name = ?''', (name,))
        nums = cursor.fetchone()
        list_nums= nums[0].split(";")
        for i in list_nums:
            fd2.append(i)
    print("\n"*5)


    # CHECK IF EQUIVALENCE NOW
    if(set(fd1) == set(fd2)):
        print("THE TWO SETS OF FDs F1 AND F2 ARE EQUIVALENT.")
    else:
        print("THE TWO SETS OF FDs F1 AND F2 ARE NOT EQUIVALENT.")
   
    print()
    # DO YOU WANT TO CONTINUE
    print("DO YOU WANT TO CONTINUE?")
    decision = input("ENTER 'Q' or 'q' to Exit or Anything Else to continue: ")
    if(decision == 'q' or decision == 'Q'):
        logout()



#validates the table the user selects to be normalized
def bcnf_initial():
    global connection, cursor
   # GET THE NAMES OF EACH TABLE
    cursor.execute('''
        select * from inputRelationSchemas; ''')
    connection.commit()
    nums = cursor.fetchall()
    names = []
    for num in nums:
        names.append(num[0])


    print("\n"*60)
    print("BCNF NORMALIZATION ")
    print("---" * 50)
    print()
    bcnf_names = []


    # GET NAMES
    print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS THE TABLE TO BE NORMALIZED")
    print("---" * 50)
    # PRINT THE TABLES
    printTables()
    print(names)
    # VALIDATE CHOICES
    while True:
        choice = input("ENTER NAME OR ENTER 'D' or 'd' WHEN DONE: ")
        print(choice)
        if (choice == "d" or choice == "D"):
            break
        
        elif choice in names and choice not in bcnf_names:
            bcnf_names.append(choice)
            bcnf(choice)

        else:
            print("TRY AGAIN,", end=" ")


#normalizing the table selected 
def bcnf(choice):
    global connection, cursor
    print('Normalizing table',choice)
    print("\n"*10)
    cursor.execute('SELECT FDs FROM inputRelationSchemas WHERE Name = ?',(choice,))
    fd = cursor.fetchone()

     #first we find our keys
    find_key(fd)

def find_key(fd):
    fd_A = []
    list_nums= fd[0].split(";")
    for i in list(list_nums)[:]:
        print(i)
        fd_A.append(i)

    print(fd_A)


   


'''#all attributes that show up only on the lefthand side
    L = []

    #all attributes that show up on both the middle and the left hand side
    M = []

    # all attribye that shows up on both the middle and the left hand side
    R = []

    #contains all attributes on the right hand side of our fd
    fd_R = []

    #contains all attributes on the left hand side of our fd
    fd_L =[]

    fd_A = []
    fd_A.append(fd[0])
    for i in fd_A:
        print(i.split())
'''


        



   




    #then we find our functional dependencies that violate bcnf
    #then we decompose them





#checks to see if s given table is dependency preserving after normalization
def dependency_preserving():
    if True:
        print("Dependecy preserving")
    else:
        print("Not dependency preserving")




 



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------PRINT TABLES FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Print the table names in the database
def printTables():
    global connection, cursor
    cursor.execute('''
        select * from inputRelationSchemas;
    ''')
    connection.commit()
    nums = cursor.fetchall()

    title=["Name","Attributes", "FDs"]
    print("%s %s %s " % (title[0].ljust(30), title[1].ljust(30), title[2].ljust(30)))
    print("---"*50)
    for num in nums:
        names= num[0]
        attributes = num[1]
        fd = num[2]
        print("%s %s %s " % (names.ljust(30), attributes.ljust(30), fd.ljust(30)))
    print("---" * 50)
    


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------MAIN FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main function
def main():
    global connection, cursor
    print("\n"*60)
    filename = input("ENTER THE FILENAME OF THE DATABASE OR ENTER 'Q' OR 'q' TO QUIT: ")

    # EXIT THE PROGRAM IF THE USER WANTS TO QUIT
    if filename == "Q" or filename == 'q':
        logout()

    #filename = "test.sqliteDB"
    
    # Initialized the path to the database
    connection = sqlite3.connect("./" + filename)
    # Set the cusor to the cursor of the database
    cursor = connection.cursor()

    # Print all the tasks a user can do
    # Validate user input
    while(True):
        # Print the tasks 
        print("\n"*60)
        print("SELECT ONE OF THE FOLLOWING TASKS: ")
        print("---" * 20)
        print("1. BCNF Normalization and Decomposition")
        print("2. Attribute Closures")
        print("3. Equivalence of 2 Sets of Functional Dependencies")
        print("---" * 20)

        # Enter a decision
        decision = input("ENTER A NUMBER OR ENTER 'Q' OR 'q' TO QUIT:: ")
    
        # EXIT THE PROGRAM IF THE USER WANTS TO QUIT
        if(decision == "q" or decision=="Q"):
            logout()
        # GO TO BCNF FUNCTION
        elif(decision == "1"):
            bcnf_initial()
            break

        # GO TO CLOSOURE FUNCTION
        elif(decision == "2"):
            closure()

        # GO TO EQUIVALENCE FUNCTION
        elif(decision == "3"):
            equivalence()
            


main()
    
