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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------EQUIVALENCE CLASS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

        while True:
            invalid= False
            # PRINT THE TABLES
            printTables()
            # VALIDATE CHOICES
            print("NOTE: SEPARATE MULTIPLE SCHEMAS WITH COMMA")
            chosen_schema = input("ENTER SCHEMA NAME(S) FOR F1: ")
            
            item=[]
            word=""
            for j in chosen_schema:
                if (j== ","):
                    item.append(word)
                    word=""
                if(j!="{" and j!="}"  and j!= "," and j!=" " and j!=""):
                    word= word+ j
            item.append(word)
           
            for i in item:
                if i not in self.table_names:
                    invalid= True
                    break

            if (invalid==False):
                self.f1_names=item
                break
  
    # set F2 NAMES
    def init_f2_names(self):
        print("\n"*5)
        print("---" * 50)
        print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS F2")
        print("---" * 50)

        while True:
            invalid= False
            # PRINT THE TABLES
            printTables()
            # VALIDATE CHOICES
            print("NOTE: SEPARATE MULTIPLE SCHEMAS WITH COMMA")
            chosen_schema = input("ENTER SCHEMA NAME(S) FOR F2: ")
            
            item=[]
            word=""
            for j in chosen_schema:
                if (j== ","):
                    item.append(word)
                    word=""
                if(j!="{" and j!="}"  and j!= "," and j!=" " and j!=""):
                    word= word+ j
            item.append(word)
           
            for i in item:
                if i not in self.table_names:
                    invalid= True
                    break

            if (invalid==False):
                self.f2_names=item
                break

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

    # GET NAMES
    print("SELECT ONE OR MORE SCHEMAS FROM THE TABLE InputRelationSchemas AS THE TABLE TO BE NORMALIZED")
    print("---" * 50)
    # PRINT THE TABLES
    printTables()

    while True:
         # VALIDATE CHOICES
        choice = input("ENTER NAME OR ENTER Q TO QUIT: ")

        if (choice == "q" or choice == "Q"):
            logout()

        elif choice in names:
            bcnf_table(choice)
            
        else:
            print("TRY AGAIN,", end=" ")


#grab our functional dependecies and attributes from the table
def bcnf_table(choice):
    candidate_keys = []
    global connection, cursor
    print('--------------------------------NORMALIZING THE TABLE-----------------------------')
    print("\n"*10)
    cursor.execute('SELECT FDs FROM inputRelationSchemas WHERE Name = ?',(choice,))
    FD = cursor.fetchone()
    FD= FD[0]
    FD_list=[]
    FD_list.append(FD)

    left_list = []
    right_list = []
    char = ''
    for FD in FD_list:
        i = 0
        str = ""
        FD_set = set()
        while i <= len(FD):
            if i != len(FD):
                char = FD[i]
            else:
                right_list.append(FD_set)
                FD_set = ()
                break
            if char != '{' and char != '}' and char != '>' and char != '=' and char != ';' and char != ',' and char != ' ':
                str = str + char
            elif char == ',' or char == '}':
                FD_set.add(str)
                str = ""
            elif char == ';':
                right_list.append(FD_set)
                FD_set = set()
                str = ""
            elif char == '=':
                left_list.append(FD_set)
                FD_set = set()
                str = ""
            i = i + 1
   
    # GEt the attriibutes
    cursor.execute('SELECT Attributes FROM inputRelationSchemas WHERE Name = ?',(choice,))
    list_attributes = cursor.fetchone()

    str_att=list_attributes[0]
    attributes= getAttr(str_att)

    #we base our closure over all the atrributes that were given
    #in our functional dependencies
    #in order to find our candidate keys we need to find the closure of 
    #our attributes on our lefthand side

    for i in left_list:
        if set(closure_BCNF(i,left_list, right_list)) == set(attributes):
            candidate_keys.append(list(i))
            
    a=[]
    violation = []
    v = []
    w = []


    for i in range(len(left_list)):
        a.append(list(left_list[i]))
        a.append(list(right_list[i]))
        r = list(zip(a[0::2],a[1::2]))

    for i in r:
        if len(i[1]) > 1:
            for j in i[1]:
                v.append(i[0])
                v.append(list(j))
        else:
            for k in i[1]:
                w.append(i[0])
                w.append(list(k))
    
    #singleton dependencies
    singles = v+w

    #now we have all our keys and we can check if we violate bcnf
    #here we check if our fd's are in bcnf
    #every attribute on the lhs of a fd must be a key
    #if not we have a violation and we need to put our table in bcnf
    violation = []

    R = list(zip(singles[0::2],singles[1::2]))
    
    #these are the functional dependecies that violate bcnf
    fd_singleton = zip(singles[0::2],singles[1::2])

    for i in list(fd_singleton):
        if i[0] not in candidate_keys:
            violation.append(i[0])
            violation.append(i[1])
        #need our candidate keys functional dependencies

    violations = list(zip(violation[0::2],violation[1::2]))

    if violations == []:
        print("TABLE IS ALREADY IN BCNF")
        return 

    else:
        bcnf(violations,candidate_keys,R)


def getAttr(schema_attributes):
    index=0
    str=""
    schema_attributes_set= set()
    while index <= len(schema_attributes):
        if index == len(schema_attributes):
            schema_attributes_set.add(str)
            index = 0
            str = ""
            break
        else:
            char = schema_attributes[index]
        if char == ',':
            schema_attributes_set.add(str)
            str = ""
        else:
            str = str+char
        index = index + 1

    attr=list(schema_attributes_set)
    attr=sorted(attr)
    return attr
   


#decompose the functional dependencies that violate bcnf
def bcnf(violation,candidate_keys,R):

    tables=[]

    keys = []
    fd_violations = []
    violations_1 = []
    a = []
    r = []
    v =[]
   

    for x in violation:
        print(x)
    # if len(x[1]) == 1:
    #     violations_1.append(x[1])
    # else:
    #     for j in x[1]:
    #         violations_1.append(j)


    # print(violations_1)
    # for i in singles:
    #     print(i)
    #     if i in violations_1:
    #         singles[singles.index(i)] = ''
    # fd_singleton = list(zip(singles[0::2],singles[1::2]))

    # print(fd_singleton)


    # #check to see if our list of violations are in bcnf
    # violations = list(zip(violation[0::2],violation[1::2]))
    # attributes_v = []
    # for i in violation:
    #     if i not in attributes_v:
    #         if len(i) == 1:
    #             attributes_v.append(i)
    #         else:
    #             for j in i:
    #                 attributes_v.append(j)

    # for i in list(violations):
    #     #find our candidate keys
    #     if closure_BCNF(i[0],choice) == attributes_v:
    #         if i[0] not in keys:
    #             keys.append(i[0])

    #     #if we have any fd's where the attribute on the lhs is not a key
    #     #we add it to a list and will later decompose it 
    #     if i[0] not in keys:
    #         v.append(i[0])
    #         v.append(i[1])
    # #if we have violations we decompose our violations list
    # if v != []:
    #     bcnf_violations(v,singles)
    # #else we print our normalized functional dependecies 
    # else:
    #     violations_v_1 = zip(violation[0::2],violation[1::2])
    #     for i in list(violations_v_1):
    #         if len(i[1]) == 1:
    #             v.append(i[1])
    #         else:
    #             for j in i[1]:
    #                 v.append(j)
    #         if i not in fd_violations:
    #             fd_violations.append(i)

    #     print_outputFDs(fd_singleton,fd_violations)
    #     dependency_preserving(singles,violation,R)


def bcnf_violations(v,keys,singles,R):
    violations_v_1 = zip(v[0::2],v[1::2])
    violation_rhs = []

    #get all the attributes on the rhs of our violating functional dependencies
    for i in violation_v_1:
        if i[1] not in violation_rhs:
            violation_rhs.append(i[1])
    v =[]
    fd_violations = []
    #while not bcnf:
    for i in singles:
        if i in violations_rhs:
            singles[singles.index(i)] = ''
    fd_singleton = zip(singles[0::2],singles[1::2])

    for i in list(violations_v_1):
        if len(i[1]) == 1:
            v.append(i[1])
        else:
            for j in i[1]:
                v.append(j)
        if i not in fd_violations:
            fd_violations.append(i)

    print_outputFDs(fd_singleton,fd_violations)
    dependency_preserving(singles,v,R)

#checks to see if s given table is dependency preserving after normalization
#dependency preserving if the closure of R = closure of R1 union R2
def dependency_preserving(singles,v,R):
    attributes_R = []
    attributes_R1 = []
    attributes_R2 = []
    
    #computing the closure of R
    for i in list(R):
        if len(i[0]) == 1 and i[0] not in attributes_R:
            attributes_R.append(i[0])
        if len(i[1]) == 1 and i[1] not in attributes_R:
            attributes_R.append(i[0])
        if len(i[1]) >1:
            for j in i[1] and j not in attributes_R:
                attributes_R.append(j)
        if len(i[0])>1:
            for j in i[0]:
                if j not in attributes_R:
                    attributes_R.append(j)
        closure_R = closure_BCNF(i[0],attributes_R)

    #computing the closure of R1
    fd_singleton = zip(singles[0::2],singles[1::2]) 
    for i in list(fd_singleton):
        if len(i[0]) == 1 and i[0] not in attributes_R1:
            attributes_R1.append(i[0])
        if len(i[1]) == 1 and i[1] not in attributes_R1:
            attributes_R1.append(i[0])
        if len(i[1]) >1:
            for j in i[1] and j not in attributes_R1:
                attributes_R1.append(j)
        if len(i[0])>1:
            for j in i[0]:
                if j not in attributes_R1:
                    attributes_R1.append(j)
        closure_R1 = closure_BCNF(i[0],attributes_R1)
 

    #computing the closure of R2
    fd_violations = zip(v[0::2],v[1::2])
    for i in list(fd_violations):
        if len(i[0]) == 1 and i[0] not in attributes_R2:
            attributes_R2.append(i[0])
        if len(i[1]) == 1 and i[1] not in attributes_R2:
            attributes_R2.append(i[0])
        if len(i[1]) >1:
            for j in i[1] and j not in attributes_R2:
                attributes_R2.append(j)
        if len(i[0])>1:
            for j in i[0]:
                if j not in attributes_R2:
                    attributes_R2.append(j)
        closure_R2 = closure_BCNF(i[0],attributes_R2)


    if closure_R == closure_R1+closure_R2:
        print("THE RELATION IS DEPENDENCY PRESERVING")
        print('\n'*35)

    else:
        print("THE RELATION IS NOT DEPENDENCY PRESERVING")
        print('\n'*35)

   
def print_outputFDs(fd_singleton,fd_violations):
    r = []
    a = []
    k = []
    for i in fd_violations:
        if i[0] != '':
            i = i[0]+"=>"+i[1]
            r.append(i)

    #output the normalized functional dependencies
    for i in fd_singleton:
        if i[0]!='':

            i = i[0]+"=>"+i[1]
            a.append(i)

    print('\n'*60)

    #print R1
    print('---------------------------------------R1----------------------------------------')
    print()
    print(a)
    print()
    print('---------------------------------------------------------------------------------')

    print('\n'*3)

    #print R2
    print('---------------------------------------R2----------------------------------------')
    print()
    print(r)
    print()
    print('---------------------------------------------------------------------------------')
    print()



def closure_BCNF(attribute, left_list, right_list):
    closure = set()
    closure=attribute
    old = set()
    index = 0
    while True:
        old = closure
        for index in range(0, len(left_list)):
            if left_list[index].issubset(closure) and not (right_list[index].issubset(closure)):
                closure = closure.union(right_list[index])
        if old.issubset(closure) and closure.issubset(old):
            break
    
    closure = list(closure)
    closure=sorted(closure)
    return closure 




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------CLOSURE CLASS-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def closure():
    global connection, cursor
    
    schema_list = []
    #ALLOW THE USER TO ENTER SCHEMAS
    while True:
        str = ""
        printTables()
        print("NOTE: SEPARATE MULTIPLE SCHEMAS WITH COMMA")
        chosen_schema = input("ENTER SCHEMA NAME(S): ")
        i = 0
        char=''
        while i <= len(chosen_schema):
            if i == len(chosen_schema):
                schema_list.append(str)
            else:
                char = chosen_schema[i]
            if char != ',' and char != " ":
                str = str + char
            elif char == ',':
                schema_list.append(str)
                str = ""
            i = i+1
        invalid = 0
        for schema in schema_list:
            cursor.execute('''select * 
                            from InputRelationSchemas 
                            where Name = ?''', (schema,))
            valid_schema = cursor.fetchone()
            if not valid_schema:
                invalid = 1
        if invalid != 1:
            print()
            print()
            break
        else:
            print()
            print()
            print("PLEASE CHOOSE VALID SCHEMA(S)!")
            schema_list = []

    attribute_list = []
    str = ""
    index = 0
    schema_attributes_set = set()

    #PUT THE ATTRIBUTES FOR THE CHOSEN SCHEMA INTO A SET
    for i in schema_list:
        cursor.execute('''select Attributes 
                        from InputRelationSchemas 
                        where Name = ?''', (i,))
        schema_attributes = cursor.fetchone()
        schema_attributes = schema_attributes[0]
        while index <= len(schema_attributes):
            if index == len(schema_attributes):
                schema_attributes_set.add(str)
                index = 0
                str = ""
                break
            else:
                char = schema_attributes[index]
            if char == ',':
                schema_attributes_set.add(str)
                str = ""
            else:
                str = str+char
            index = index + 1

    #ALLOW THE USER TO CHOOSE ATTRIBUTES FOR CLOSURE CALCULATION
    chosen_attributes_set = set()
    while True:
        att_str = "{"
        print("AVAILABLE ATTRIBUTES: ")
        print("--"*50)
        counter = 0
        strings=[]
        for i in schema_list:
            cursor.execute('''  select Attributes  
                                from InputRelationSchemas
                                where Name = ?''', (i,))
            att = cursor.fetchone()
            att = att[0]

            # GET chars
            word=""
            items=[]
            for j in att:
                if (j== ","):
                    items.append(word)
                    word=""

                elif(j!="{" and j!="}"  and j!= "," and j!="" and j!=" "):
                    word= word+ j
            items.append(word)
            for i in items:
                if i not in strings:
                    strings.append(i)
           

        strings.sort()
        for i in strings:
            if (counter==len(strings)-1):
                 att_str = att_str + i + '}'
            else:
                att_str = att_str + i + ','
                counter = counter + 1
       
       

        print("GIVEN ATTRIBUTES: ", att_str)
        print("--"*50)
        print("NOTE: SEPARATE MULTIPLE ATTRIBUTES WITH COMMA")
        chosen_attributes = input("ENTER SUBSET OF GIVEN ATTRIBUTES: ")
        print()
        i = 0
        c=''
        while i <= len(chosen_attributes):
            if i == len(chosen_attributes):
                chosen_attributes_set.add(str)
            else:
                c = chosen_attributes[i]
            if c != ',' and i!=len(chosen_attributes):
                str = str+c
            elif c == ',':
                chosen_attributes_set.add(str)
                str = ""
            i = i + 1
        
        if chosen_attributes_set.issubset(schema_attributes_set):
            chosen_attributes_list = sorted(chosen_attributes_set)
            break
        else:
            print("PLEASE ENTER VALID ATTRIBUTES")
            chosen_attributes_set = set()
            str=""

    #GET THE FD'S FROM CHOSEN SCHEMAS AND INSERT THEM INTO A LIST
    FD_list = []
    for i in schema_list:
        cursor.execute('''  select FDs
                            from InputRelationSchemas
                            where Name = ?''', (i,))
        FD = cursor.fetchone()
        FD = FD[0]
        FD_list.append(FD)
        connection.commit()

    #SEPARATE THE LEFT HAND SIDE AND RHS OF FD INTO TWO LISTS
    left_list = []
    right_list = []
    for FD in FD_list:
        i = 0
        str = ""
        FD_set = set()
        while i<=len(FD):
            if i != len(FD):
                char = FD[i]
            else:
                right_list.append(FD_set)
                FD_set = ()
                break
            if char != '{' and char != '}' and char != '>' and char != '=' and char !=';' and char != ',' and char != ' ':
                str = str + char
            elif char == ',' or char == '}':
                FD_set.add(str)
                str = ""
            elif char == ';':
                right_list.append(FD_set)
                FD_set = set()
                str = ""
            elif char == '=':
                left_list.append(FD_set)
                FD_set = set()
                str = ""
            i = i+1

    #CALCULATE THE CLOSURE FOR THE CHOSEN ATTRIBUTES
    closure = set()
    closure = chosen_attributes_set
    old = set()
    index = 0
    while True:
        old = closure
        for index in range(0,len(left_list)):
            if left_list[index].issubset(closure) and not (right_list[index].issubset(closure)):
                closure = closure.union(right_list[index])
        if old.issubset(closure) and closure.issubset(old):
            break
    sorted_closure = sorted(closure)

    #PREPARE THE CLOSURE AND CHOSEN ATTRIBUTES FOR PRINTING
    closure_str = "{"
    i = 0
    while i< len(sorted_closure):
        if i == len(sorted_closure)-1:
            closure_str = closure_str + sorted_closure[i] + '}'
        else:
            closure_str = closure_str + sorted_closure[i] + ','
        i = i+1
    i = 0

    attr_str = "{"
    while i < len(chosen_attributes_list):
        if i == len(chosen_attributes_list) -1:
            attr_str = attr_str + chosen_attributes_list[i] + '}'
        else:
            attr_str = attr_str + chosen_attributes_list[i] + ','
        i = i + 1



    #PRINT THE CLOSURE
    print("--"*50)
    print("THE ATTRIBUTE CLOSURE OF", attr_str, "IS: ", closure_str)
    print("--"*50)
    print()
    decision = input("PRESS Q TO EXIT OR PRESS ANY KEY TO CONTINUE: ")
    if decision == 'q' or decision == 'Q':
        logout()
    

 



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
    
