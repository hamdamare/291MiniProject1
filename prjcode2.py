import sqlite3
import datetime
import time
import random

# CITATIONS: 
# https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list 
# https://stackoverflow.com/questions/8866652/determine-if-2-lists-have-the-same-elements-regardless-of-order
# http://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
# https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-given-a-list-containing-it-in-python
# https://www.geeksforgeeks.org/equivalence-of-functional-dependencies-sets/

# Global variables
connection = None
cursor = None

#------------------------------------EQUIVALENCE CLASS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Checks to see the Equivalence of 2 Sets of Functional Dependencies
class equivalence:

    # Attributes of the equivalence class
    def __init__(self):
        self.f1_names=[]
        self.f2_names=[]
        self.table_names=[]

        # Attributes
        self.chars1=[]
        self.chars2=[]

        # X and y for x-->y in F1
        self.fd1_x=[]
        self.fd1_y=[]
        self.x1=[]
        self.y1=[]

        # X and y for x-->y in F2
        self.fd2_x=[]
        self.fd2_y=[]
        self.x2=[]
        self.y2=[]

        self.equivalent=True

    # set THE NAMES OF EACH TABLE
    def init_table_names(self):
        global connection, cursor

        cursor.execute('''
            select * from inputRelationSchemas; ''')
        connection.commit()
        nums = cursor.fetchall()
        for num in nums:
            self.table_names.append(num[0])

    # set F1 NAMES
    def init_f1_names(self):
        # GET F1 NAMES
        print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS F1")
        print("---" * 50)
        # PRINT THE TABLES
        printTables()
        # VALIDATE CHOICES
        while True:
            choice = input("ENTER NAME OF TABLE TO ADD TO F1 OR PRESS ENTER WHEN DONE: ")
            if (choice == "" or choice == ""):
                break
            elif (choice in self.table_names and choice not in self.f1_names):
                self.f1_names.append(choice)
            else:
                print("TRY AGAIN,", end=" ")

    # set F2 NAMES
    def init_f2_names(self):
        print("\n"*5)
        print("---" * 50)
        print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS F2")
        print("---" * 50)
        # PRINT THE TABLES
        printTables()
        # VALIDATE CHOICES
        while True:
            choice = input("ENTER NAME OF TABLE TO ADD TO F2 OR PRESS ENTER WHEN DONE: ")
            if (choice == "" or choice == ""):
                break
            elif (choice in self.table_names and choice not in self.f2_names):
                self.f2_names.append(choice)
            else:
                print("TRY AGAIN,", end=" ")

    # set THE attributes FOR F1 and F2
    def init_attributes(self):
        attribute1=self.getAttributes(self.f1_names)
        #Grab characters only for attribute1
        self.chars1=self.getCharsOnly(attribute1)

        attribute2=self.getAttributes(self.f2_names)
        #Grab characters only for attribute2
        self.chars2=self.getCharsOnly(attribute2)


    # set THE FDs FOR F1 and F2
    def init_fds(self):
        # GET F1 only
        fd1=self.getFDs(self.f1_names)
        for i in range(len(fd1)):
            new_list=fd1[i].split("=>")
            self.fd1_x.append(new_list[0])
            self.fd1_y.append(new_list[1])
        #Grab characters only
        self.x1=self.getCharsOnly(self.fd1_x)
        self.y1=self.getCharsOnly(self.fd1_y)


         # GET F2 only
        fd2=self.getFDs(self.f2_names)
        for i in range(len(fd2)):
            new_list=fd2[i].split("=>")
            self.fd2_x.append(new_list[0])
            self.fd2_y.append(new_list[1])
        #Grab characters only
        self.x2=self.getCharsOnly(self.fd2_x)
        self.y2=self.getCharsOnly(self.fd2_y)
    
    
    # Checking whether all FDs of FD1 are present in FD2
    def equalivalence_check1(self):
        i=0
        while(i<len(self.fd1_x) and self.equivalent==True):
            # If present in FD1 but not directly in FD2 but we will check whether we can derive it or not. 
            if(self.fd1_x[i] not in self.fd2_x or self.fd1_y[i] not in self.fd2_y):
                #Check to see if the FD1_y is in the closure of FD1_x in Relation2
                attr=[]

                # Get the initial attributes in the closure of the fd
                # Append all of the attributes in x1[i] into attr
                for items in self.x1[i]:
                    for item in items:
                        attr.append(item)  

                # Add to attr if the elements in attr are in x2 as a whole
                count=0
                for j in self.x2:
                    if(all(x in attr for x in j)):
                        item=self.y2[count]
                        item= "".join(item)
                        if (item not in attr):
                            attr.append(item)
                    count=count+1
          
                # Equivalence Check
                # check to see if attr contains y1[i]
                if(not all(x in attr for x in self.y1[i]) ):
                    self.equivalent=False
            i=i+1

    # Checking whether all FDs of FD2 are present in FD1
    def equalivalence_check2(self):
        i=0
        while(i<len(self.fd2_y) and self.equivalent==True):
            # If present in FD2 but not directly in FD1 but we will check whether we can derive it or not. 
            if(self.fd2_x[i] not in self.fd1_x or self.fd2_y[i] not in  self.fd1_y):
                #Check to see if the FD1_y is in the closure of FD1_x in Relation2
                attr=[]

                # Get the initial attributes in the closure of the fd
                # Append all of the attributes in x1[i] into attr
                for items in self.x2[i]:
                    for item in items:
                        attr.append(item)  
        
                # Add to attr if the elements in attr are in x2 as a whole
                count=0
                for j in self.x1:
                    if(all(x in attr for x in j)):
                        item=self.y1[count]
                        item= "".join(item)
                        if (item not in attr):
                            attr.append(item)
                    count=count+1

                # Equivalence Check
                # check to see if attr contains y1[i]
                if(not all(x in attr for x in self.y2[i]) ):
                    self.equivalent=False

            i=i+1


    def done(self):
        print("\n"*5)

        # CHECK IF EQUIVALENCE NOW
        if(self.equivalent):
            print("THE TWO SETS OF FDs F1 AND F2 ARE EQUIVALENT.")
        else:
            print("THE TWO SETS OF FDs F1 AND F2 ARE NOT EQUIVALENT.")
    

     # GET THE FDs FOR a list of table names (Returns list )
    def getFDs(self, list_items):
        global connection, cursor

        items=[]
        for i in list_items:
            cursor.execute('''
            select FDs 
            from InputRelationSchemas
            where Name = ?''', (i,))
            connection.commit()
            nums = cursor.fetchone()
            list_nums= nums[0].split(";")

            for j in list_nums:
                items.append(j)
        return items

    # GET the attributes FOR a list of table names (Returns list )
    def getAttributes(self, list_items):
        global connection, cursor

        items=[]
        for i in list_items:
            cursor.execute('''
            select  Attributes
            from InputRelationSchemas
            where Name = ?''', (i,))
            connection.commit()
            nums = cursor.fetchone()
            list_nums= nums[0].split(";")

            for j in list_nums:
                items.append(j)
        return items

    # Grab characters only for a list containing strings (Returns list of lists)
    def getCharsOnly(self, list_items):
        items=[]
        for i in list_items:
            item=[]
            word=""
            for j in i:
                if (j== ","):
                    item.append(word)
                    word=""
                if(j!="{" and j!="}"  and j!= "," and j!=" "):
                    word= word+ j
            item.append(word)
            items.append(item)
        return items



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
   
    while True:
         # VALIDATE CHOICES
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

    cursor.execute('SELECT Attributes FROM inputRelationSchemas WHERE Name = ?',(choice,))
    attributes = cursor.fetchone()
     #first we find our keys
    find_key(fd,attributes)

def find_key(fd,attributes):
    fd_x = []
    fd_y=[]
    list_nums= fd[0].split(";")
    for i in list(list_nums)[:]:
        new_list=i.split("=>")
        fd_x.append(new_list[0])
        fd_y.append(new_list[1])


    #Grab characters only
    x=[]
    for i in fd_x:
        name=""
        for j in i:
            if(j!="{" and j!="}" and j!="," and j!=" "):
                name=name+j
        x.append(name)

    y=[]
    for i in fd_y:
        name=""
        for j in i:
            if(j!="{" and j!="}" and j!="," and j!=" "):
                name=name+j
        y.append(name)


    for i in range(len(x)):
        a=[]
        a.append(x[i])
        a.append(y[i])
        for j in range(i+1, len(x)):
            for k in a:
                if (k==x[j]):
                    a.append(y[i])
        print(a)




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
#------------------------------------logout FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Terminate the program
def logout():
    exit(0)



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

    filename = "test.sqliteDB"
    
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

        # GO TO EQUIVALENCE class call
        elif(decision == "3"):
            print("\n"*60)
            print("Equivalence of 2 Sets of Functional Dependencies ")
            print("---" * 50)
            print()

            # Make an instance of equivalence
            equal= equivalence()

            # call to init table names
            equal.init_table_names()
            # call to set the fds of f1
            equal.init_f1_names()
            # call to set the fds of f2
            equal.init_f2_names()

            # call to set the attributes for f1 and f2
            equal.init_attributes()
            # call to set the fds of f1 and f2
            equal.init_fds()

            # Checking whether all FDs of FD1 are present in FD2
            equal.equalivalence_check1()
            # Checking whether all FDs of FD2 are present in FD1
            equal.equalivalence_check2()

            # Call to display results, if two sets are equivalent or not
            equal.done()


            print()
            # DO YOU WANT TO CONTINUE
            print("DO YOU WANT TO CONTINUE?")
            decision = input("ENTER 'Q' or 'q' to Exit or Anything Else to continue: ")
            if(decision == 'q' or decision == 'Q'):
                logout()



main()
    
