# WORK DONE BY AYUB AHMED, HAMDA MARE, AND HAMSE MARE

# Citations:

# Import modules
from hashlib import pbkdf2_hmac
import time
import sqlite3
import datetime
import time
import random

# Global variables
connection = None
cursor = None

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ACCOUNT MANAGER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# linkes account managers to the many options account managers have
#add the enter q to logout statement
def account_manager(username):
    global connection, cursor
    print("\n"*55)
    print("-------------------------------------------------------------")
    print("ACCOUNT MANAGER PAGE:")
    print("-------------------------------------------------------------")
    print( 'Welcome Account Manager ')
    print("ENTER q to EXIT")

    print ()
    while True:

        print('What would you like to do?')
        print('Enter 1: to view the customer information of all customers that you manage:\nEnter 2: to create a new customer account:\nEnter 3: to create a new service agreement for an existing customer:\nEnter 4: to view a customers summary: ')
        options=input("OPTION: ")

        if(options=="q" or options=="Q"):
            logout()

        elif options =='1':
            account_managerQ1(username)
            break

        elif options == '2':
            account_managerQ2(username)
            break

        elif options == '3':
            account_managerQ3(username)
            break

        elif options == '4':
            account_managerQ4(username)
            break
        else:
            print()
            print('Incorrect option selected')
            continue

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------FUNCTION CHECKS FOR VALID PHONE NUMBER FORMAT------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#checks for valid phonenumber format
def valid_contact(contact_info):
    if len(contact_info) != 12:
        return False
    else:
        for i in range(12):
            if i in[3,7]:
                if contact_info[i]!= '-':
                    return False
            elif contact_info[i].isalpha():
                return False
            
        return True

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 1----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def account_managerQ1(username):
    global connection, cursor
    # We select the customer information of all the customers that the user manages
    #then we run our query which outputs the customer information that this manager manages
    t1= (username)
    cursor.execute('''
            SELECT a.customer_name, a.contact_info,a.customer_type,s.service_no,s.master_account, s.location,s.waste_type,s.pick_up_schedule,s.local_contact,s.internal_cost,s.price 
            FROM accounts a, service_agreements s, account_managers m, personnel p 
            WHERE p.name=? AND p.pid = m.pid AND m.pid = a.account_mgr AND s.master_account = a.account_no ORDER BY s.service_no''', (t1,))
    customer_info = cursor.fetchall()
    if customer_info!=[]:
        #print the customer information
        print()
        for i in customer_info:
            print("CUSTOMER NAME: ", i[0], "  CONTACT INFO: ", i[1], "   CUSTOMER TYPE: ", i[2], "   SERVICE NO: ", i[3], 
                  "   MASTER ACCOUNT: ", i[4], "    LOCATION: ", i[5],   "WASTE TYPE: ", i[6], "  PICK UP SCHEDULE: ", i[7], "   LOCAL CONTACT: ", i[8], "   INTERNAL COST: ", i[9], 
                  "   PRICE: ", i[10])

        print('\n\nWhat would you like to do?\n')
        option = input("Enter q to exist or anything else to return back to the homepage: ")

        if (option == 'q' or option == 'Q'):
            logout()
    else:
        print()
        print()
        print("No customer information of all the customers that the user manages!!!")
        time.sleep(2)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 2----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Q2- user adds a new customer account to the database
def account_managerQ2(username):
    global connection, cursor
    #Create a new master account with all the required information. The manager of the account should be automatically set to the id of the account manager who is creating the account.
    #first we select the id of the account manager with the manager name equal to the login name

    cursor.execute('SELECT  user_id FROM users WHERE login = ?', (username,))
    connection.commit()
    uid=cursor.fetchone()[0]

    t1=(uid,)
    cursor.execute('SELECT  m.pid, a.account_no FROM personnel p, account_managers m, accounts a WHERE m.pid=a.account_mgr and p.pid = m.pid AND p.pid = ?', (t1))
    connection.commit()
    info = cursor.fetchall()

    list_account_nums=[]
    for i in info:
        i=list(i)
        list_account_nums.append(i[1])


    for i in info:
        #grab new customer information from user 
        print()
        while True:
            account_no = input('ENTER AN ACCOUNT NUMBER(8 DIGITS): ')
            if (account_no=="q" or account_no=="Q"):
                logout()

            #make sure its len is 8 
            if len(account_no) != 8 or account_no in list_account_nums:
                print("TRY AGAIN,", end=" ")
                continue
            break

        
        #Get the start date
        while True:
            start_date= input("ENTER START DATE (FORMAT YYYY-MM-DD): ")
            if (start_date=="q" or start_date=="Q"):
                logout()
            
            date_list= start_date.split("-")  
            if(len(date_list)!=3):
                print("TRY AGAIN,", end=" ")
                continue

            # GET THE YEAR
            year=date_list[0]
            if len(year)!=4:
                print("TRY AGAIN,", end=" ")
                continue

            # GET THE MONTH
            month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
            month=date_list[1]

            if len(month)==2 and month[0]=="0":
                month=month[1]

            if month not in month_list:
                print("TRY AGAIN,", end=" ")
                continue
        
            # GET THE DAY
            day=date_list[2]
            
            if len(day)==2 and day[0]=="0":
                day=day[1]

            day=int(day)
            if day>31 or day<=0:
                print("TRY AGAIN,", end=" ")
                continue

            # Validate the date the user entered
            date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')

            if(datetime.datetime.now()>=date):
                print("TRY AGAIN,", end=" ")
                continue

            break

        #Get the end date
        print("\n\n")
        while True:
            end_date= input("ENTER END DATE (FORMAT YYYY-MM-DD): ")
            if (end_date=="q" or end_date=="Q"):
                logout()
            
            date_list= end_date.split("-")  
            if(len(date_list)!=3):
                print("TRY AGAIN,", end=" ")
                continue

            # GET THE YEAR
            year=date_list[0]
            if len(year)!=4:
                print("TRY AGAIN,", end=" ")
                continue

            # GET THE MONTH
            month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
            month=date_list[1]

            if len(month)==2 and month[0]=="0":
                month=month[1]

            if month not in month_list:
                print("TRY AGAIN,", end=" ")
                continue
        
            # GET THE DAY
            day=date_list[2]

            if len(day)==2 and day[0]=="0":
                day=day[1]
                
            day=int(day)
            if day>31 or  day<=0:
                print("TRY AGAIN,", end=" ")
                continue

            # Validate the date the user entered
            end_date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')
            
            start_list= start_date.split("-")  
            start_d= datetime.datetime.strptime(start_list[0]+'-'+start_list[1]+'-'+start_list[2], '%Y-%m-%d')

            if(start_d>=end_date):
                print("TRY AGAIN,", end=" ")
                continue

            break



        #make sure customer name is not null
        while True:
            customer_name = input('ENTER A CUSTOMER NAME: ')
            if (customer_name=="q" or customer_name=="Q"):
                logout()

            if len(customer_name) == 0 or not customer_name.isalpha():
                print("TRY AGAIN,", end=" ")
                continue
            break


        #make sure customer type is one of the types that we have
        while True:
            print('SELECT ONE OF THE FOLLOWING CUSTOMER TYPES:')
            print()
            print('1.COMMERCIALl\n2.INDUSTRIAL\n3.MUNICIPAL\n4.RESIDENTIAL')
            print()
            customer_type = input('ENTER 1, 2, 3, or 4: ')
            if (customer_type=="q" or customer_type=="Q"):
                logout()

            if customer_type == '1':
                Type = 'commercial'
                break

            elif customer_type == '2':
                Type = 'industrial'
                break

            elif  customer_type== '3':
                Type=='municipal'
                break

            elif customer_type == '4':
                Type = 'residential'
                break

            else:
                print("TRY AGAIN,", end=" ")
                continue
            break

        #make contact info is correct fix in class
        while True:
            print()
            contact_info = input('ENTER CUSTOMER CONTACT INFO (FORMAT 000-000-0000): ')
            if (contact_info=="q" or contact_info=="Q"):
                logout()

            if valid_contact(contact_info) == False:
                print("TRY AGAIN,", end=" ")
                continue
            break
            


        #make sure user enters a total amount
        while True:
            print()
            total_amount = input('Enter a total amount: ')
            if (total_amount=="q" or total_amount=="Q"):
                logout()

            if (len(total_amount)==0 or total_amount.isalpha()):
                print("TRY AGAIN,", end=" ")
                continue
            break
        

    
        # now create a new customer account with the manager id
        cursor.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?);', (str(account_no,),str(uid),str(customer_name,),str(contact_info,),str(Type,),str(start_date,),str(end_date,),str(total_amount,)))
        connection.commit()
        print('...........')
        print('New Customer Account Created!')
        print()


        #ask user if they want to add a service agreement to either an existing customer or a customer already int he database
        print('Would you like to create a service agreement for this customer?')
        #pause a bit
        create_sa = input('Enter Y for Yes or N for No: ')
        print()
        #if account manager does not want to add a service agreement to a new customer we ask if they would like to add one for any other customers they manage
        if (create_sa == 'N' or create_sa =='n'):
            print()
            print('Would you like to create a service agreement for any other customers?')
            sa = input('Enter Y for Yes or anything else to quit: ') 
            #if yes we add a service agreement to the another customer 
            if (sa == 'Y' or sa == 'y'):
                account_managerQ3(username);
            else:
                logout()
                

        #if user chooses to create a service agreement for the newly added customer
        elif (create_sa == 'Y' or create_sa =='y'):
            #select all the service numbers that we have 
            while True:
                location = input('Enter a location: ')
                if(location == 'q' or location == 'Q'):
                    logout()
                elif len(location) < 3:
                    print("TRY AGAIN,", end=" ")
                    continue
                break

            #check for valid waste type
            while True:
                print()
                print('SELECT ONE OF THE FOLLOWING')
                option = input('ENTER 1: hazardous waste\nENTER 2: mixed waste\nENTER 3: construction waste\nENTER 4: metal\nENTER 5: compost\nENTER 6: paper\nENTER 7: plastic: ')
                
                if (option=="q" or option=="Q"):
                    logout()

                elif option == '1':
                    waste_type = 'hazardous waste'
                    break

                elif option == '2':
                    waste_type = 'mixed waste'
                    break

                elif option == '3':
                    waste_type = 'construction waste'
                    break

                elif option == '4':
                    waste_type = 'metal'
                    break

                elif option == '5':
                    waste_type = 'compost'
                    break

                elif option == '6':
                    waste_type = 'paper'
                    break

                elif option == '7':
                    waste_type = 'plastic'
                    break
                elif (option == 'Q' or option == 'q'):
                    logout()
                else:
                    print("TRY AGAIN,", end=" ")
                    continue


            #testcase for pickup schedule
            while True:
                print()
                print('SELECT FROM ONE OF THE FOLLOWING PICK UP SCHEDULES\n')
                print('1: Every Monday of every week\n2: Every Tuesday of every week\n3: Every Wednesday of every week\n4: Every Friday of every week\n5: Every Saturday of every week')

                pick_up_schedule = input('Enter a pick up schedule: ')
                if (pick_up_schedule=="q" or pick_up_schedule=="Q"):
                    logout()

                elif pick_up_schedule == '1':
                    pick_up_schedule = 'Every Monday of every week'
                    break

                elif pick_up_schedule == '2':
                    pick_up_schedule = 'Every Tuesday of every week'
                    break

                elif pick_up_schedule == '3':
                    pick_up_schedule = 'Every Wednesday of every week'
                    break

                elif pick_up_schedule == '4':
                    pick_up_schedule = 'Every Thursday of every week'
                    break

                elif pick_up_schedule == '5':
                    pick_up_schedule = 'Every Friday of every week'
                    break

                else:
                    print("TRY AGAIN,", end=" ")
                    continue


            #testcase for local contact
            while True:
                print()
                local_contact = input('Enter a local contact (FORMAT 000-000-0000):  ')
                if (local_contact=="q" or local_contact=="Q"):
                    logout()

                elif valid_contact(local_contact)!= True:
                    print("TRY AGAIN,", end=" ")
                    continue
                break

            #check for valid internal cost
            while True:
                print()
                internal_cost = input('Enter the internal cost: ')

                if (internal_cost=="q" or internal_cost=="Q"):
                    logout()

                elif (len(internal_cost)==0 or internal_cost.isalpha()):
                    print("TRY AGAIN,", end=" ")
                    continue
                break

            #check for valid price
            while True:
                print()
                price = input('Enter a price: ')
                if (price == 'Q' or price == 'q'):
                    logout

                elif (len(price) == 0 or price.isalpha()):
                    print("TRY AGAIN,", end=" ")
                    continue
                break


            master_account = account_no

            #check if inputed customer info is valid 
            cursor.execute('SELECT service_no FROM service_agreements')
            connection.commit()
            badSA = cursor.fetchall()

            # GENERATE SERVICE NO
            #randomly select a service number 
            service_no = random.randint(0,100)
            otherSA=[]
            for i in badSA:
                otherSA.append(i[0])
            # MAKE SURE UNIQUE
            while(service_no in otherSA):
                service_no = random.randint(0,100)


            #create the service agreement
            cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(master_account,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))
            connection.commit()

            time.sleep(0.2)
            print ('..........')
            print('\nService Agreement Created!')

            #user chooses to return to account manager page or logout
            print()
            option = input("Enter q to exit or anything else to return back to the homepage: ")
            if (option == 'q' or option == 'Q'):
                logout()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 3----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Q3-if user decides to create a service agreement for a customer that already exists 
def account_managerQ3(username):
    #First we get the manager id for the account manager
    cursor.execute('SELECT  user_id FROM users WHERE login = ?', (username,))
    connection.commit()
    uid=cursor.fetchone()[0]

    t1=(uid,)

    #print all the custoemers an account manaager manages
    print("\nTHESE ARE ALL THE CUSTOMERS YOU MANAGE:")
    cursor.execute('SELECT a.customer_name,a.account_no  FROM accounts a, personnel p, account_managers m WHERE m.pid = p.pid and m.pid = a.account_mgr and p.pid = ?', (t1))
    connection.commit()
    customer_info= cursor.fetchall()
    #select customer name
    if customer_info == []:
        print('You do not have any customers yet.')
        print()

    else:

        print('Customer names \t\tAccount number')
        print("--"*20)
        nums=[]
        for i in customer_info:
            customer_names = i[0]
            #select customer number
            customer_nums = i[1]
            nums.append(customer_nums)
            print(customer_names.ljust(20), end="\t")
            print(customer_nums)


        while True:
            #then we get the customer who the account manager wants to make a service agreeement for
            customer_num = input('\nWhat is the account number of the customer you want to select: ')
            if (customer_num == 'q' or customer_num == 'Q'):
                logout()

            #check to see if customer_num is coorect
            elif (customer_num not in nums):
                print('TRY AGAIN!')
                continue
            break
        
        #initialize account number as the enterd customer number
        a_no = customer_num 
        #account manager selects a customer they manage and we grab service agreement information
        #randomly select a service number 
        #check if inputed customer info is valid 
        cursor.execute('SELECT service_no FROM service_agreements')
        connection.commit()
        badSA = cursor.fetchall()

        # GENERATE SERVICE NO
        #randomly select a service number 
        service_no = random.randint(0,100)
        otherSA=[]
        for i in badSA:
            otherSA.append(i[0])
        # MAKE SURE UNIQUE
        while(service_no in otherSA):
            service_no = random.randint(0,100)

        
        #check for valid location
        while True:
            print()
            location = input('Enter a location: ')
            if(location == 'q' or location == 'Q'):
                logout()
            elif len(location) < 3:
                print("TRY AGAIN,", end=" ")
                continue
            break

        #check for valid waste type
        while True:
            print()
            print('Select from one of the following')
            print('1.hazardous waste\n2.mixed waste\n3.construction waste\n4.metal\n5.compost\n6.paper\n7.plastic: ')
            option=input("ENTER: ")
            if (option  == 'q' or option  == 'Q'):
                logout()

            elif option == '1':
                waste_type = 'hazardous waste'
                break

            elif option == '2':
                waste_type = 'mixed waste'
                break

            elif option == '3':
                waste_type = 'construction waste'
                break

            elif option == '4':
                waste_type = 'metal'
                break

            elif option == '5':
                waste_type = 'compost'
                break

            elif option == '6':
                waste_type = 'paper'
                break

            elif option == '7':
                waste_type = 'plastic'
                break
       
            else:
                print("TRY AGAIN,", end=" ")
                continue


        #testcase for pickup schedule
        while True:
            print()
            print('SELECT FROM ONE OF THE FOLLOWING PICK UP SCHEDULES')
            print('1.Every Monday of every week\n2.Every Tuesday of every week\n3.Every Wednesday of every week\n4.Every Friday of every week\n5.Every Saturday of every week')
            print()
            pick_up_schedule = input('Enter a pick up schedule: ')
            if (pick_up_schedule  == 'q' or pick_up_schedule  == 'Q'):
                logout()


            elif pick_up_schedule == '1':
                pick_up_schedule = 'Every Monday of every week'
                break

            elif pick_up_schedule == '2':
                pick_up_schedule = 'Every Tuesday of every week'
                break

            elif pick_up_schedule == '3':
                pick_up_schedule = 'Every Wednesday of every week'
                break

            elif pick_up_schedule == '4':
                pick_up_schedule = 'Every Thursday of every week'
                break

            elif pick_up_schedule == '5':
                pick_up_schedule = 'Every Friday of every week'
                break

            else:
                print("TRY AGAIN,", end=" ")
                continue

        #testcase for local contact
        while True:
            print()
            local_contact = input('Enter a local contact (FORMAT 000-000-0000): ')
            if (local_contact  == 'q' or local_contact  == 'Q'):
                logout()

            elif valid_contact(local_contact)!= True:
                print("TRY AGAIN,", end=" ")
                continue
            break

        #check for valid internal cost
        while True:
            print()
            internal_cost = input('Enter the internal cost: ')
            if (internal_cost  == 'q' or internal_cost  == 'Q'):
                logout()
            elif (len(internal_cost)==0 or internal_cost.isalpha()):
                print("TRY AGAIN,", end=" ")
                continue
            break

        #check for valid price
        while True:
            print()
            price = input('Enter a price: ')
            if (price  == 'q' or price  == 'Q'):
                logout()
            elif (price == 'Q' or price == 'q'):
                logout
            elif (len(price) == 0 or price.isalpha()):
                print("TRY AGAIN,", end=" ")
                continue
            break


        #if the information is valid then we create a service agreement account for this customer
        cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(a_no,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))
        connection.commit()
        time.sleep(0.2)
        print ('..........')
        print('\nService Agreement Created!')

    #user chooses to return to account manager page or logout
    print()
    option = input("Enter q to exit or anything else to return back to the homepage: ")
    if (option == 'q' or option == 'Q'):
        logout()
        

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 4----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q4 prints the summary for a single  customer                   
def account_managerQ4(username):
    cursor.execute('SELECT  user_id FROM users WHERE login = ?', (username,))
    connection.commit()
    uid=cursor.fetchone()[0]

    t1=(uid,)

    #print all the custoemers an account manaager manages
    print("\nTHESE ARE ALL THE CUSTOMERS YOU MANAGE:")
    cursor.execute('SELECT a.customer_name,a.account_no  FROM accounts a, personnel p, account_managers m WHERE m.pid = p.pid and m.pid= a.account_mgr and p.pid = ?', (t1))
    connection.commit()
    customer_info= cursor.fetchall()

    if (customer_info == []):
        print('You do not have any customers yet.')
        print()
        

    else:

        print('Customer names \t\tAccount number')
        print("--"*20)
        nums=[]
        for i in customer_info:
            customer_names = i[0]
            #select customer number
            customer_nums = i[1]
            nums.append(customer_nums)
            print(customer_names.ljust(20), end="\t")
            print(customer_nums)


        while True:
            #then we get the customer who the account manager wants to make a service agreeement for
            customer_num = input('\nWhat is the account number of the customer you want to see a summary report for: ')
            if (customer_num == 'q' or customer_num == 'Q'):
                logout()

            #check to see if customer_num is coorect
            elif (customer_num not in nums):
                print('TRY AGAIN!')
                continue
            break


        account_no = customer_num


        #select the count of services, sum of internal cost, sum of prices, and the count of the different waste types
        cursor.execute('SELECT COUNT(s.service_no), SUM(s.internal_cost),SUM(s.price) FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = a.account_no AND a.account_no =?' ,(account_no,))
        connection.commit()
        summary = cursor.fetchall()



        cursor.execute('SELECT COUNT(*)  FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = ? GROUP BY s.waste_type' ,(account_no,))
        connection.commit()
        waste_types = cursor.fetchall()


        #print the summary for the user and the number of distinct waste_types
        distinct_types = len(waste_types)
        summarys = []
        for i in summary:
            i=list(i)
            for j in range(3):
                summarys.append(i[j])

        summarys.append(distinct_types)

        print("SUMMARY")
        #print the summary for the user and the number of distinct waste_types
        print("--"*40)
        print("TOTAL NUMBER OF SERVICE AGREEMENTS:", summarys[0], "       SUM OF PRICES: ", summarys[1],  "       SUM OF INTERNAL COST:", summarys[2], "          NUMBER OF DIFFERNET WASTE TYPES:", summarys[3])


    #user chooses to return to account manager page or logout
    print()
    option = input("Enter q to exit or anything else to return back to the homepage: ")
    if (option == 'q' or option == 'Q'):
        logout()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------SUPERVISOR FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Supervisor(username):
    global cursor, connection

    print("\n"*55)
    print("-------------------------------------------------------------")
    print("Welcome Supervisor!\n")
    print("-------------------------------------------------------------")

    ##Get the user_id of the logged in supervisor
    cursor.execute('''SELECT user_id FROM users where login = ?''', (username,))
    supervisor_pid = cursor.fetchone()
    connection.commit()

    #Allow the user to choose from a range of 3 options or press q to exit
    while True:
        print('Enter q to exit!')
        print('Enter m:  Create a new master account')
        print("Enter s:  Summary report for single customer")
        print("Enter a:  Summary of account managers")
        print()
        decision = input("Enter one of the given letters above: ")

        if decision == 'q' or decision=='Q':
            logout()
        elif decision == 'm' or decision == 'M':
            create_master_account(supervisor_pid)
        elif decision == 's' or decision == 'S':
            summary_customer(supervisor_pid)
        elif decision == 'a' or decision == 'A':
            summary_account_manager(supervisor_pid)

        else:
            continue

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------Question 1----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# This function creates a new master account with one of the account managers under the supervisor
# This function creates a new master account with one of the account managers under the supervisor
def create_master_account(supervisor_pid):
    global connection, cursor

    while True:
        print("AVAILABLE MANAGER PID")
        print("--" * 80)
        cursor.execute('''SELECT p.name, m.pid
                         FROM personnel p, account_managers m
                         WHERE m.pid = p.pid
                         AND p.supervisor_pid = ?''', supervisor_pid)
        # Find all the managers under this supervisor
        available_managers = cursor.fetchall()
        connection.commit()
        for i in available_managers:
            print("MANAGER NAME: ", i[0], "     PID: ", i[1])
        print("--" * 80)
        # allow the user to choose one of the managers
        manager = input("ENTER MANAGER PID:")

        if (manager  == 'q' or manager  == 'Q'):
            logout()

        t1 = supervisor_pid + (manager,)
        # Check if the chosen manager exists within the table
        cursor.execute('''SELECT p.pid
                            FROM account_managers a, personnel p
                            WHERE p.pid = a.pid
                            AND p.supervisor_pid = ?
                            AND p.pid = ?''', t1)
        exists = cursor.fetchall()
        connection.commit()
        if exists != []:
            break
        print("INCORRECT MANAGER PID PLEASE TRY AGAIN\n")

    while True:
        account_number = input("Enter an account number of length 8:")

        if (account_number  == 'q' or account_number  == 'Q'):
            logout()

        # account number must be a length of 8
        # check if the account number already exists in the table
        cursor.execute('''SELECT a.account_no
                            FROM accounts a
                            WHERE a.account_no = ?''', (account_number,))
        account_exists = cursor.fetchall()
        connection.commit()
        if account_exists == [] and len(account_number) == 8:
            break
        print("That account number has already been taken or is invalid please try again")


    # get the pertinent information for the new account
    
    #Get the start date
    print("\n\n")
    while True:
        start_date= input("ENTER START DATE (FORMAT YYYY-MM-DD): ")
        if (start_date=="q" or start_date=="Q"):
            logout()
        
        date_list= start_date.split("-")  
        if(len(date_list)!=3):
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE YEAR
        year=date_list[0]
        if len(year)!=4:
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE MONTH
        month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
        month=date_list[1]

        if len(month)==2 and month[0]=="0":
            month=month[1]

        if month not in month_list:
            print("TRY AGAIN,", end=" ")
            continue
    
        # GET THE DAY
        day=date_list[2]
        
        if len(day)==2 and day[0]=="0":
            day=day[1]

        day=int(day)
        if day>31 or  day<=0:
            print("TRY AGAIN,", end=" ")
            continue

        # Validate the date the user entered
        date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')

        if(datetime.datetime.now()>=date):
            print("TRY AGAIN,", end=" ")
            continue

        break

    #Get the end date
    print("\n\n")
    while True:
        end_date= input("ENTER END DATE (FORMAT YYYY-MM-DD): ")
        if (end_date=="q" or end_date=="Q"):
            logout()
        
        date_list= end_date.split("-")  
        if(len(date_list)!=3):
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE YEAR
        year=date_list[0]
        if len(year)!=4:
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE MONTH
        month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
        month=date_list[1]

        if len(month)==2 and month[0]=="0":
            month=month[1]

        if month not in month_list:
            print("TRY AGAIN,", end=" ")
            continue
    
        # GET THE DAY
        day=date_list[2]

        if len(day)==2 and day[0]=="0":
            day=day[1]
            
        day=int(day)
        if day>31 or  day<=0:
            print("TRY AGAIN,", end=" ")
            continue

        # Validate the date the user entered
        end_date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')
        
        start_list= start_date.split("-")  
        start_d= datetime.datetime.strptime(start_list[0]+'-'+start_list[1]+'-'+start_list[2], '%Y-%m-%d')

        if(start_d>=end_date):
            print("TRY AGAIN,", end=" ")
            continue

        break

    customer_name = input("Enter the customer name: ")
    if (customer_name  == 'q' or customer_name  == 'Q'):
        logout()
   
    #testcase for local contact
    while True:
        print()
        contact_info = input("Enter the contact info (FORMAT 000-000-0000): ")
        if (contact_info  == 'q' or contact_info  == 'Q'):
            logout()
        elif valid_contact(contact_info)!= True:
            continue
        break

    print()
    print("CUSTOMER TYPE")
    print("--"*30)  
    print("industrial") 
    print("commercial") 
    print("municipal")
    print("residential")
    print()
    customer_type = input("Enter the customer type: ")
    if (customer_type  == 'q' or customer_type  == 'Q'):
        logout()

    while True:
        if customer_type == "industrial" or customer_type=="commercial" or customer_type=="municipal" or customer_type=="residential":
            break
        

    #make sure user enters a total amount
    while True:
        print()
        total_amount = input('Enter a total amount: ')
        if (total_amount=="q" or total_amount=="Q"):
            logout()

        elif (len(total_amount)==0 or total_amount.isalpha()):
            print("TRY AGAIN,", end=" ")
            continue
        break
        

    # create the account
    cursor.execute('INSERT INTO accounts VALUES(?,?,?,?,?,?,?,?)', (
    account_number, manager, customer_name, contact_info, customer_type, start_date, end_date, total_amount))
    connection.commit()
    print("\n"*3)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------Question 2-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def summary_customer(supervisor_pid):
    global cursor, connection
    cursor.execute(
        '''SELECT p.name FROM personnel p, account_managers a WHERE a.pid = p.pid AND p.supervisor_pid = ?''',
        supervisor_pid)
    managers = cursor.fetchall()
    connection.commit()
    # allow the user to choose from the available managers they supervise
    print("AVAILABLE MANAGERS:\n")
    print("--" * 80)
    for i in managers:
        print("MANAGER NAME: ", i[0])
    print("--" * 80)
    while True:
        manager_selection = input("PLEASE SELECT ONE OF THE MANAGERS:")
        if (manager_selection=="q" or manager_selection=="Q"):
            logout()

        t1 = supervisor_pid + (manager_selection,)
        cursor.execute('''SELECT p.name 
        FROM account_managers a, personnel p
        WHERE a.pid = p.pid
        AND p.supervisor_pid = ?
        AND p.name = ?''', t1)
        chosen_manager = cursor.fetchall()
        connection.commit()
        # check if we have duplicate names and ask the user to specify the PID
        if len(chosen_manager) >= 2:
            while True:
                cursor.execute(
                    '''SELECT p.pid FROM account_managers a, personnel p WHERE a.pid = p.pid AND p.supervisor_pid = ? AND p.name = ?''',
                    t1)
                duplicate_managers = cursor.fetchall()
                connection.commit()
                print("DUPLICATE MANAGER PLEASE SPECIFY PERSONNEL ID FROM BELOW:")
                print("--" * 80)
                for i in duplicate_managers:
                    print("MANAGER NAME: " + manager_selection + "   PID:", i[0])
                print("--" * 80)
                # allow the user to further specify the manager they wanted to choose
                chosen_pid = input("SELECT MANAGER PID:")

                if (chosen_pid=="q" or chosen_pid=="Q"):
                    logout()


                list_managers=[]
                for i in duplicate_managers:
                    i=list(i)
                    list_managers.append(i[0])

                if chosen_pid in list_managers:
                    manager_selection = chosen_pid
                    break
            break

        else:
            # if the manager exists we get their PID
            if chosen_manager != []:
            
                cursor.execute('''SELECT p.pid
                FROM personnel p, account_managers a
                WHERE  a.pid = p.pid
                AND p.supervisor_pid = ?
                AND p.name=?''', t1)
                manager_selection = cursor.fetchone()[0]
                connection.commit()
                break
            # the chosen manager does not exist we loop back to check again
            print("INVALID MANAGER CHOICE PLEASE TRY AGAIN\n")

            print("AVAILABLE MANAGERS:")
            print("--" * 80)
            for i in managers:
                print("MANAGER NAME: ", i[0])
            print("--" * 80)


    # print out the available customers for the user to choose
    print("AVAILABLE CUSTOMERS:")
    print("--" * 80)
    chosen_manager = chosen_manager[0]
    cursor.execute('''SELECT a.customer_name FROM accounts a, personnel p WHERE p.pid=a.account_mgr and a.account_mgr = ?''',(manager_selection,))
    available_customers = cursor.fetchall()
    connection.commit()

    if (available_customers==[]):
        print("There are no customers for this account manager")
        logout()

    for i in available_customers:
        print("Customer name: ", i[0])
    print("--" * 80)

    while True:
        # The user enters the customer for which they wish to see the summary
        customer_selection = input("PLEASE SELECT ONE OF THE CUSTOMERS: ")
        if (customer_selection=="q" or customer_selection=="Q"):
            logout()

        cursor.execute('''SELECT customer_name FROM accounts WHERE account_mgr = ?''', (manager_selection,))
        chosen_customer = cursor.fetchall()

        # we check if there are duplicates of the customer name and allow the user to further specify with account no
        t4=(manager_selection,)+(customer_selection,)
        cursor.execute('''Select account_no from accounts where account_mgr = ? and customer_name=?''', t4)
        check_dup = cursor.fetchall()
        connection.commit()
        if len(check_dup) >= 2:
            while True:
                cursor.execute('''SELECT account_no
                FROM accounts
                WHERE account_mgr = ?
                AND customer_name = ?''', t4)
                account_numbers = cursor.fetchall()
                connection.commit()

                # print out the choices for the user
                print("DUPLICATE CUSTOMER NAMES CHOOSE ACCOUNT NUMBER FROM BELOW\n")
                print("--" * 80)
                for i in account_numbers:
                    print("NAME: " + customer_selection + "     ACCOUNT NUMBER: " + i[0])
                print("--" * 80)
                # user chooses the account which they would like to see
                account_chosen = input("PLEASE ENTER ACCOUNT NUMBER:")

                if (account_chosen=="q" or account_chosen=="Q"):
                    logout()

                t5 = (customer_selection,) + (manager_selection,) + (account_chosen,)
                cursor.execute('''SELECT account_no
                FROM accounts a
                WHERE customer_name = ?
                AND account_mgr = ?
                AND account_no = ?''', t5)
                customer_account = cursor.fetchall()
                connection.commit()

                # check if it exists, if so then exit loop
                if customer_account != []:
                    customer_account = customer_account[0]
                    break
            break

        else:
            # if the customer exists we get their account number
            customers=[]
            for i in chosen_customer:
                i=list(i)
                customers.append(i[0])

           
            if chosen_customer != [] and customer_selection in customers:
                cursor.execute('''SELECT a.account_no
                FROM accounts a
                WHERE a.account_mgr = ?
                AND a.customer_name = ?''', t4)

                customer_account = cursor.fetchone()
                connection.commit()
                break

        # if customer does not exist we show the available customers and loop back
        print("AVAILABLE CUSTOMERS:")
        print("--"*80)

        for i in available_customers:
            print("Customer name: " + i[0])
        print("--" * 80)


    # compile the summary for the chosen customer
    cursor.execute('''SELECT count(s.service_no), sum(s.price), sum(s.internal_cost)
                    FROM service_agreements s
                    WHERE s.master_account = ?
                    GROUP BY s.waste_type''', customer_account)

    summary = cursor.fetchall()
    connection.commit()

    # find the number of different waste types for the chosen customer
    cursor.execute('''SELECT count(*)
    FROM service_agreements s
    WHERE s.master_account = ?
    GROUP BY s.waste_type''', customer_account)
    waste_types = cursor.fetchall()
    connection.commit()
    number_types = len(waste_types)

    # print out the summary
    if summary!=[]:
        for i in summary:
            print("ACCOUNT MANAGER: ", name, "   NUMBER OF SERVICE AGREEMENTS: ", i[0], "    SUM OF PRICES: ", i[1],
                  "   SUM OF INTERNAL COST: ", i[2], "    NUMBER OF WASTE TYPES: ", number_types)
    else:
        print()
        print("NO DATA AVAILABLE FOR CUSTOMER")
    print("\n"*3)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------QUESTION 3--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def summary_account_manager(supervisor_pid):
    global connection, cursor
    # find the information for the summary of all account managers
    cursor.execute('''
        SELECT p.name, count(master_account), count(service_no), sum(price), sum(internal_cost)
        FROM service_agreements s, personnel p, accounts ac
        WHERE p.supervisor_pid = ? AND p.pid = ac.account_mgr AND ac.account_no = s.master_account
        GROUP BY p.pid
        ORDER BY (sum(price)-sum(internal_cost))''', supervisor_pid)
    row = cursor.fetchall()
    connection.commit()
    # print out the summary
    print("MANAGER ACCOUNT SUMMARY:")
    print("--" * 80)
    for i in row:
        print("ACCOUNT MANAGER:", i[0], "       NUMBER OF SERVICE AGREEMENTS: ", i[1], "        SUM OF PRICES: ", i[2],
              "       SUM OF INTERNAL COST:", i[3])
    print("\n"*3)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------DRIVER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Drivers must be able to perform the following task:
# For a given date range, list all the tours that they have been assigned to. The information about a tour consists of the the following:
# The location where to exchange containers.
# The local contact information for the service agreement.
# The waste_type involved in the service agreement.
# The container ID of the container to be dropped off.
# The container ID of the container to be picked up.
def driver(username):
    global connection, cursor

    print("\n"*55)
    print("-------------------------------------------------------------")
    print("WELCOME DRIVER!!")
    print("-------------------------------------------------------------")
    print('Enter q to exit!')

    #Get the start date
    print("\n\n")
    while True:
        start_date= input("ENTER START DATE (FORMAT YYYY-MM-DD): ")
        if (start_date=="q" or start_date=="Q"):
            logout()
        
        date_list= start_date.split("-")  
        if(len(date_list)!=3):
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE YEAR
        year=date_list[0]
        if len(year)!=4:
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE MONTH
        month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
        month=date_list[1]

        if len(month)==2 and month[0]=="0":
            month=month[1]

        if month not in month_list:
            print("TRY AGAIN,", end=" ")
            continue
    
        # GET THE DAY
        day=date_list[2]
        
        if len(day)==2 and day[0]=="0":
            day=day[1]

        day=int(day)
        if day>31 or  day<=0:
            print("TRY AGAIN,", end=" ")
            continue

        # Validate the date the user entered
        date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')

        if(datetime.datetime.now()>=date):
            print("TRY AGAIN,", end=" ")
            continue

        break


    #Get the end date
    print("\n\n")
    while True:
        end_date= input("ENTER END DATE (FORMAT YYYY-MM-DD): ")
        if (end_date=="q" or end_date=="Q"):
            logout()
        
        date_list= end_date.split("-")  
        if(len(date_list)!=3):
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE YEAR
        year=date_list[0]
        if len(year)!=4:
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE MONTH
        month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
        month=date_list[1]

        if len(month)==2 and month[0]=="0":
            month=month[1]

        if month not in month_list:
            print("TRY AGAIN,", end=" ")
            continue
    
        # GET THE DAY
        day=date_list[2]

        if len(day)==2 and day[0]=="0":
            day=day[1]
            
        day=int(day)
        if day>31 or  day<=0:
            print("TRY AGAIN,", end=" ")
            continue

        # Validate the date the user entered
        end_date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')
        
        start_list= start_date.split("-")  
        start_d= datetime.datetime.strptime(start_list[0]+'-'+start_list[1]+'-'+start_list[2], '%Y-%m-%d')

        if(start_d>=end_date):
            print("TRY AGAIN,", end=" ")
            continue

        break

    cursor.execute('''
        select user_id
        from users
        where login=?''', username)
    connection.commit()
    uid=cursor.fetchone()[0]
    print(uid)


    t=(start_date, end_date, uid)
    cursor.execute('''
        SELECT sa.location, sa.local_contact, sa.waste_type, s.cid_drop_off, s.cid_pick_up  
        from service_agreements sa, service_fulfillments s
        where sa.master_account=s.master_account
        and s.service_no=sa.service_no
        and s.date_time>=? 
        and s.date_time<=?
        and s.driver_id=?''', t)
    connection.commit()
    rows=cursor.fetchall()

    # Display Tours formatted
    print("\n\n\n")
    print("INFORMATION ABOUT THE TOUR CONSISTS OF THE FOLLOWING: ")
    values=["LOCATION", "LOCAL CONTACT", "WASTE TYPE", "DROP OFF CONTAINER ID ", "PICK UP CONTAINER ID"]
    string="%10s|%10s|%10s|%10s|%10s"%(values[0].ljust(20), values[1].ljust(20), values[2].ljust(20), values[3].ljust(20), values[4].ljust(40))
    print(string)
    print("--"*80)
    service_no_list=[]

    if(rows==[]):
        print("NONE")
        
    else:
        for value in rows:
            value=list(value)
            service_no_list.append(value[0])
            formatted_string="%10s|%10s|%10s|%10s|%10s" %(value[0].ljust(20), value[1].ljust(20), value[2].ljust(20), value[3].ljust(20), value[4].ljust(40))
            print(formatted_string)

    # CONTINUE??
    print()
    print("DO YOU WANT TO CONTINUE?")
    decision= input("ENTER q TO EXIT or ANYTHING ELSE TO CONTINUE: ")
    
    if (decision=="q" or decision=="Q"):
        logout()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------DISPATCHER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dispatcher():
    global connection, cursor

    print("\n"*55)

    print("-------------------------------------------------------------")
    print("WELCOME DISPATCHER!!")
    print("-------------------------------------------------------------")
    print('Enter q to exit!')

    
    # Select a service_agreement, driver, truck, and a container to be dropped off and picked up
    
    # Select a service no for a particular service agreement
    
    service_no= Dispatcher_getService_no()

    # Find master account
    cursor.execute('''
        select s.master_account
        from service_agreements s
        where s.service_no=?''', (service_no,))
    connection.commit()
    row= cursor.fetchone()

    master_account=row[0]

    # Select a driver

    driver= Dispatcher_getDriver()

    # Select a truck depending on if the driver owns a truck, if they do then automatically truck is set
    # Else Choose a truck
    truck=Dispatcher_getTruck(driver)

    # Get the cointainer getting picked up
    cid_pick_up= Dispatcher_getPickUp(service_no)

    # Select the container being dropped off
    cid_drop_off= Dispatcher_getDropOff(service_no)

    # Set the date
    date=setDate()

    # Create entries in the table service_fulfillments for upcoming days
    add_service_fulliment(date, master_account, service_no, truck, driver, cid_drop_off, cid_pick_up)

    # CONTINUE??
    print()
    print("DO YOU WANT TO CONTINUE?")
    decision= input("ENTER q TO EXIT ANYTHING ELSE TO CONTINUE: ")

    if (decision=="q" or decision=="Q"):
        logout()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------ADD TO SERVICE FULFILLMENT TABLE------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Add the entry to the service_fulliment table with the following data
def add_service_fulliment(date_time, master_account, service_no, truck_id, driver_id, cid_drop_off, cid_pick_up):
    global connection, cursor
    cursor.execute('''
        INSERT INTO service_fulfillments VALUES(?,?,?,?,?,?,?)''',(date_time, master_account, service_no, truck_id, driver_id, cid_drop_off, cid_pick_up) )
    connection.commit()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------GET THE SERVICE NO------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get the service Agreement
def Dispatcher_getService_no():
    global connection, cursor
    
    # Get all the rows in the service agreements
    cursor.execute('''
        select *
        from service_agreements
        group by service_no
        ''')
    connection.commit()
    rows=cursor.fetchall()
    
    # Allow dispatcher to choose from it
    print("\n\n")
    print("SELECT ONE SERVICE NO FROM THE FOLLOWING SERVICE AGREEMENTS:")
    

    values=["SERVICE NO", "MASTER ACCOUNT", "LOCATION", "WASTE TYPE",  "PICK UP SCHEDULE",  "LOCAL CONTACT", "INTERNAL COST",  "PRICE"]
    string="%10s|%10s|%10s|%10s|%10s|%10s|%10s|%10s"%(values[0].ljust(20), values[1].ljust(20), values[2].ljust(20), values[3].ljust(20), values[4].ljust(40), values[5].ljust(20), values[6].ljust(20), values[7].ljust(20))
    print(string)
    print("--"*100)

    service_no_list=[]
    for value in rows:
        value=list(value)
        service_no_list.append(value[0])
        formatted_string="%10s|%10s|%10s|%10s|%10s|%10s|%-20.2f|%.2f"%(value[0].ljust(20), value[1].ljust(20), value[2].ljust(20), value[3].ljust(20), value[4].ljust(40), value[5].ljust(20), value[6], value[7])
        print(formatted_string)
        print()

    # Get the service_no and validate its correct
    while True:
        service_no=input("SELECT THE SERVICE AGREEMENT: ")
        if (service_no=="q" or service_no=="Q"):
            logout()
        if(service_no not in service_no_list):
            print("TRY AGAIN,", end=" ")
            continue
        else:
            break

    # Return the service no choosen from the dispatcher
    return service_no

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------GET THE DRIVER------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get the service Agreement
def Dispatcher_getDriver():
    global connection, cursor

    # Select all the drivers
    cursor.execute('''
        select distinct p.pid, p.name
        from drivers d, personnel p
        where p.pid= d.pid 
        ''')
    connection.commit()
    # Dispatcher can choose from it
    rows=cursor.fetchall()

    print("\n\n")
    print("SELECT ONE DRIVER FROM THE FOLLOWING DRIVERS: ")
    

    print("DRIVER ID \t     DRIVER NAME")
    print("---"*20)

    drivers_list=[]
    for value in rows:
        value=list(value)
        drivers_list.append(value[0])
        print("%s %s" %(value[0].ljust(20), value[1]))

    # Get the driver and validate its correct
    while True:
        driver=input("ENTER DRIVER ID: ")
        if (driver=="q" or driver=="Q"):
            logout()
        if(driver not in drivers_list):
            print("TRY AGAIN,", end=" ")
            continue
        else:
            break
    return driver


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------Question 1------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# If a driver is selected who owns a truck, that truck should be automatically selected; 
# otherwise the dispatcher also must select a truck.
def Dispatcher_getTruck(driver):
    global connection, cursor
    
    # SEARCH TO SEE IF THE DRIVER HAS A TRUCK OR NOT
    cursor.execute('''
        select distinct owned_truck_id
        from drivers 
        where pid=?''', (driver,))
    connection.commit()
    num=cursor.fetchone()[0]

    # IF the driver has no trucks then do the following
    if(num==None):
        
        # Get the Trucks Not owned by the company
        cursor.execute('''
            select distinct truck_id, model
            from trucks
            group by truck_id
            
            EXCEPT 

            SELECT t.truck_id, t.model
            FROM trucks t, drivers d
            WHERE d.owned_truck_id=t.truck_id
            GROUP BY t.truck_id''')

        connection.commit()
        trucks=cursor.fetchall()
            
        print("\n\n")
        print("SELECT A TRUCK FROM THE FOLLOWING TRUCKS: ")
    
        print("TRUCK ID \t     MODEL")
        print("---"*20)

        truck_list=[]
        for value in trucks:
            value=list(value)
            truck_list.append(value[0])
            print("%s %s" %(value[0].ljust(20), value[1]))


        # Get the truck and validate its correct
        while True:
            truck=input("ENTER TRUCK ID: ")

            if (truck=="q" or truck=="Q"):
                logout()

            if(truck not in truck_list):
                print("TRY AGAIN,", end=" ")
                continue
            else:
                break

    else:
        # GET THE TRUCK
        truck= num
    
    return truck


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------Question 2------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get the container that were picking up
def Dispatcher_getPickUp(service_no):
    global connection, cursor

    #Query to get the location associated with the service no
    cursor.execute('''
        select distinct location
        from service_agreements
        where service_no=?''', (service_no,))
    connection.commit()
    loc=cursor.fetchone()[0]
    
    # Select only cointainer at the location of the service no
    cursor.execute('''
        SELECT c.container_id
        FROM containers c
        WHERE EXISTS (
            SELECT *
            FROM service_fulfillments s, service_agreements sa
            WHERE s.cid_drop_off = c.container_id
            AND sa.master_account=s.master_account
            AND sa.location=?
            ORDER BY s.date_time desc limit 2)''', (loc,))
    connection.commit()
    
    # Get the container thats gonna be picked up
    # DO checks
    container=cursor.fetchall()
    list_containers=[]
    for i in container:
        i=list(i)
        for j in i:
            list_containers.append(j)

    if(len(list_containers)==0 or len(list_containers)==1):
        container= '0000'
    else:
        container=list_containers[1]

    # Return the container to be picked up 
    return container


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------Question 3------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get the container that were dropping off
def Dispatcher_getDropOff(service_no):
    global connection, cursor

    #Query to get the waste type associated with the service no
    cursor.execute('''
        select distinct waste_type
        from service_agreements
        where service_no=?''', (service_no,))
    connection.commit()
    waste_type=cursor.fetchone()[0]


    # Select all containers that are available and hold the appropriate waste type, given in the service agreement.
    cursor.execute('''
            SELECT c.container_id
            FROM container_waste_types c
            WHERE NOT EXISTS (SELECT *
                              FROM service_fulfillments s
                              WHERE s.cid_drop_off = c.container_id)
            AND c.waste_type=?
            UNION
            SELECT c.container_id
            FROM containers c
            WHERE (SELECT MAX(date_time) FROM service_fulfillments s WHERE s.cid_pick_up = c.container_id)
                   >
                  (SELECT MAX(date_time) FROM service_fulfillments s WHERE s.cid_drop_off = c.container_id)''', (waste_type,))
    
    connection.commit()
    rows=cursor.fetchall()

    # Display the containers to the dispatcher
    print("\n\n")
    print("SELECT ONE CONTAINER FROM THE FOLLOWING CONTAINERS: ")
    
    print("CONTAINER ID ")
    print("--"*10)

    container_list=[]
    for value in rows:
        value=list(value)
        container_list.append(value[0])
        print("%s" %(value[0].ljust(20)))

    # Get the container and validate its correct
    while True:
        container=input("ENTER CONTAINER ID: ")

        if (container=="q" or container=="Q"):
            logout()
        if(container not in container_list):
            print("TRY AGAIN,", end=" ")
            continue
        else:
            break
    # Return the container being dropped off
    return container

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------Question 4------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Set the date for a particular entry
def setDate():
    
    date_list=[]


    print("\n\n")
    while True:
        date= input("ENTER DATE (FORMAT YYYY-MM-DD): ")
        if (date=="q" or date=="Q"):
            logout()
        
        date_list= date.split("-")  
        if(len(date_list)!=3):
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE YEAR
        year=date_list[0]
        if len(year)!=4:
            print("TRY AGAIN,", end=" ")
            continue

        # GET THE MONTH
        month_list=['1','2','3','4','5','6','7','8','9','10','11','12']

        month=date_list[1]
        if len(month)==2 and month[0]=="0":
            month=month[1]

        if month not in month_list:
            print("TRY AGAIN,", end=" ")
            continue
    
        # GET THE DAY
        day=date_list[2]

        if len(day)==2 and day[0]=="0":
            day=day[1]
            
        day=int(day)
        if day>31 or  day<=0:
            print("TRY AGAIN,", end=" ")
            continue

        # Validate the date the user entered
        date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')

        if(datetime.datetime.now()>=date):
            print("TRY AGAIN,", end=" ")
            continue

        break

    # return the date
    return date
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------FIND ROLE FUNCTION WHEN USER LOGGED IN-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function find_role returns the role associated to that particular username
def find_role(username):
    global connection, cursor

    t1= (username,)
    cursor.execute('SELECT role FROM users WHERE login=?', t1)

    role = cursor.fetchone()
    connection.commit()
    # Return the role of the user
    return role[0]

    role = cursor.fetchone()[0]
    connection.commit()
    # Return the role of the user
    return role

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------ROLE GATE KEEPER FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Depending on the role, GateKeeper for that tasks asociated to that role
def Role_GateKeeper(role, username):
    if (role=="account manager"):
        account_manager(username)
        
    elif (role== "supervisor"):
        Supervisor(username)

            
    elif (role== "dispatcher"):
        dispatcher()
            
    else:
        driver(username)
            

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------START FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Begins the main functionallity of the program, endless loop unless loop until the user 
# exits manually by entering the desired key("q") to end program
def start(username):
    print()
    while True:
        role = find_role(username)
        Role_GateKeeper(role, username)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------AUTHENTICATE FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Checks the database to authenticate what the user entered is correct
def Authenticate(entered_pwd,username):
    global connection, cursor

    status = False
    # Hashed it using code given
    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000

    t1=(username,)
    # Selects the password from the table associated to the user
    cursor.execute('SELECT password FROM users WHERE login==?',t1)
    connection.commit()
    rows = cursor.fetchall()

    # If hashed password is the same as the hashed database password then login is successful
    if(rows!=[]):
        for row in rows:
            dk=row[0]
            dk2 = encrypt_password(entered_pwd)
            if dk == dk2:
                status = True   
    return status


# Assume user is not in the users table
def encrypt_password(password):
    global connection, cursor
    status = False
    # Hashed it using code given
    hash_name = 'sha256'
    salt = 'ssdirf993lksiqb4'
    iterations = 100000
    dk =pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)

    return dk


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------LOGIN FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Allows user to log in succesfully with previous username and previous password
def login():
    print("\n"*55)
    print("-------------------------------------------------------------")
    print("LOGIN PAGE:")
    print("-------------------------------------------------------------")
    print('ENTER q to EXIT!')
    

    count=0
    while count<3:
        print("ATTEMPTS REMAINING: %d" % (3-count) )
        print()
        # If user has logged out we dont have to login
        if logout == True:
            break

        # Get username
        username = input("Please enter your Login: ")
        # Check to see if user enetered q to quit
        if (username=="q" or username=="Q"):
            logout()
        
        # Get password
        psw = input("Please enter your Password: ")
    
        
        # Check to see if user enetered q to quit
        if (psw=="q" or psw=="Q"):
            logout()

        print ('\n')
        print ('Authenticating............')
        time.sleep(0.5)

        # If hashed password is the same as the hashed database password then login is successful
        status = Authenticate(psw,username)
        # If Login is not successful, loop back to login
        if not status:
            print("Username and Password do not match\n\n")
            count=count+1
        # If the user successfully logged in we find its roles
        if status:
            start(username)
    logout()

            

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------GET ROLE FUNCTION FOR CREATING AN ACCOUNT-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets the role of a particular user
def get_role(pid):
    global cursor, connection
    # case1: Account Manager Table
    cursor.execute('''
        SELECT *
        FROM personnel p, account_managers a
        WHERE p.pid=a.pid
        AND p.pid=?''', (pid,))
    connection.commit()
    acccount_manager_table=cursor.fetchall()

    # case2: Driver Table
    cursor.execute('''
        SELECT *
        FROM personnel p, drivers d
        WHERE p.pid=d.pid
        AND p.pid=?''', (pid,))
    connection.commit()
    driver_table=cursor.fetchall()

    # case3: Supervisor
    cursor.execute('''
        SELECT *
        FROM personnel p
        WHERE p.supervisor_pid=?''', (pid,))
    connection.commit()
    supervisor_table=cursor.fetchall()

    # case1
    if acccount_manager_table!=[]:
        role="account manager"
    # case2
    elif driver_table!=[]:
        role="driver"
    # case3
    elif supervisor_table!=[]:
        role="supervisor"
    # case4
    else:
        role="dispatcher"

    return role



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------CREATE ACCOUNT FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Creates a user account with the desired information prompted to the user
def create_account():
    global cursor, connection

    print("\n"*55)
    print("-------------------------------------------------------------")
    print("CREATE ACCOUNT PAGE:")
    print("-------------------------------------------------------------")
    print('ENTER q TO EXIT!')
    
    # PID
    # Make sure that pid is in personnel
    while True:
        pid = input('Please enter your personnel identification number: ')

        if (pid=="q" or pid=="Q"):
            logout()

        # Invalid pid
        cursor.execute('''
            select *
            from personnel
            where pid=?''', (pid,))
        row=cursor.fetchall()
        connection.commit()
        if row==[]:
            print("\nPERSONNEL IDENTIFICATION NUMBER IS NOT IN THE SYSTEM!")
            continue
        
        # Account already created
        cursor.execute('''
            select *
            from users
            where user_id=?''', (pid,))
        row=cursor.fetchall()
        connection.commit()
        
        if row!=[]:
            print("\nPID ALREADY HAS A ACCOUNT!")
            continue
        break

    # USERNAME
    # Make sure the username is unique
    while True:
        username = input('Please enter a Login: ')
        if (username=="q" or username=="Q"):
            logout()
        cursor.execute('''
            select *
            from users
            where login=?''', (username,))
        connection.commit()
        row=cursor.fetchall()

        if row!=[]:
            print("\nUSERNAME IS ALREADY IN USE!")
            continue
        
        break

    # PASSWORD
    password = input('Please enter a password: ')
    if (password=="q" or password=="Q"):
        logout()

    encrypt_pass = encrypt_password(password)

    # ROLE
    role=get_role(pid)

    t=(pid,role,username,encrypt_pass)
    
    #insert user information into the users table
    cursor.execute('INSERT INTO users VALUES(?,?,?,?)',t)
    connection.commit()
    # Call to login
    print()
    print()
    login()


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------LOGOUT FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CALLS TO END PROGRAM
def logout():
    print("\n"*55)
    print("Goodbye!")
    print()
    exit(0)


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------MAIN FUNCTION-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mainn function
def main():
    global connection, cursor

    # Initialized the path to the database
    connection= sqlite3.connect("./waste_management.db")
    # Set the cusor to the cursor of the database
    cursor= connection.cursor()

    print("\n"*55)
    print("Welcome!")
    decision= input('PRESS L TO LOGIN IN, OR PRESS C TO CREATE AN ACCOUNT: ')

    if (decision=="q" or decision=="Q"):
        logout()

    elif decision == 'C' or decision== 'c':
        create_account()
    
    elif decision == 'L' or  decision=='l':
        login()

    print()
    
main()
    


