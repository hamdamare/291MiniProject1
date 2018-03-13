# WORK DONE BY AYUB AHMED, HAMDA MARE, AND HAMSE MARE

# Citations


# Import modules
from hashlib import pbkdf2_hmac
import time
import sqlite3
import datetime
import time

# Global variables
connection = None
cursor = None



# Creates the tables accessed by the system
def create_tables():
	global connection, cursor

	cursor.executescript('''
		-- The following commands drops the tables in case they exist from earlier runs. 
		DROP TABLE IF EXISTS users;
		DROP TABLE IF EXISTS service_fulfillments;
		DROP TABLE IF EXISTS service_agreements;
		DROP TABLE IF EXISTS accounts;
		DROP TABLE IF EXISTS drivers;
		DROP TABLE IF EXISTS account_managers;
		DROP TABLE IF EXISTS personnel;
		DROP TABLE IF EXISTS container_waste_types;
		DROP TABLE IF EXISTS waste_types;
		DROP TABLE IF EXISTS containers;
		DROP TABLE IF EXISTS maintenance_records;
		DROP TABLE IF EXISTS trucks;


		-- The following commands create the tables including FOREIGN KEY constraints

		CREATE TABLE users (
		  user_id	TEXT, 
		  role		TEXT,
		  login		TEXT, 
		  password	TEXT, 
		  PRIMARY KEY (user_id),
		  FOREIGN KEY (user_id) REFERENCES personnel(pid) ON DELETE CASCADE
		);


		CREATE TABLE trucks (
		  truck_id          TEXT,
		  model             TEXT,
		  truck_type        TEXT,
		  PRIMARY KEY (truck_id) 
		);

		CREATE TABLE maintenance_records (
		  truck_id          TEXT,
		  service_date      DATE,
		  description       TEXT,
		  PRIMARY KEY (truck_id, service_date),
		  FOREIGN KEY (truck_id) REFERENCES trucks ON DELETE CASCADE
		);

		CREATE TABLE containers (
		  container_id      TEXT,
		  container_type    TEXT,
		  date_when_built   DATE,
		  PRIMARY KEY (container_id)
		);

		CREATE TABLE waste_types (
		    waste_type      TEXT,
		    PRIMARY KEY (waste_type)
		);

		CREATE TABLE container_waste_types (
		  container_id      TEXT,
		  waste_type        TEXT,
		  PRIMARY KEY (container_id, waste_type),
		  FOREIGN KEY (container_id) REFERENCES containers,
		  FOREIGN KEY (waste_type) REFERENCES waste_types
		);

		CREATE TABLE personnel (
		  pid               TEXT, 
		  name              TEXT, 
		  email             TEXT, 
		  address           TEXT, 
		  supervisor_pid    TEXT, 
		  PRIMARY KEY (PID)
		);

		CREATE TABLE account_managers (
		  pid               TEXT,
		  manager_title     TEXT,
		  office_location   TEXT,
		  PRIMARY KEY (pid),
		  FOREIGN KEY (pid) REFERENCES personnel
		);

		CREATE TABLE drivers (
		  pid               TEXT,
		  certification     TEXT,
		  owned_truck_id    TEXT,
		  PRIMARY KEY (pid),
		  FOREIGN KEY (pid) REFERENCES personnel,
		  FOREIGN KEY (owned_truck_id) REFERENCES trucks(truck_id)
		);

		CREATE TABLE accounts (
		  account_no        TEXT,
		  account_mgr       TEXT,
		  customer_name     TEXT,
		  contact_info      TEXT,
		  customer_type     TEXT,
		  start_date        DATE,
		  end_date          DATE,
		  total_amount      REAL,
		  PRIMARY KEY (account_no),
		  FOREIGN KEY (account_mgr) REFERENCES account_managers(pid)
		);

		CREATE TABLE service_agreements (
		  service_no        TEXT,
		  master_account    TEXT,
		  location          TEXT,
		  waste_type        TEXT,
		  pick_up_schedule  TEXT,
		  local_contact     TEXT,
		  internal_cost     REAL,
		  price             REAL,
		  PRIMARY KEY (master_account, service_no),
		  FOREIGN KEY (master_account) REFERENCES accounts ON DELETE CASCADE, 
		  FOREIGN KEY (waste_type) REFERENCES waste_types
		); 
		  
		CREATE TABLE service_fulfillments (
		  date_time         DATE,
		  master_account    TEXT, 
		  service_no        TEXT,
		  truck_id          TEXT,
		  driver_id         TEXT,
		  cid_drop_off      TEXT,
		  cid_pick_up       TEXT,
		  PRIMARY KEY (date_time, master_account, service_no, truck_id, driver_id, cid_drop_off, cid_pick_up)
		  FOREIGN KEY (master_account, service_no) REFERENCES service_agreements,
		  FOREIGN KEY (truck_id) REFERENCES trucks,
		  FOREIGN KEY (driver_id) REFERENCES drivers(pid),
		  FOREIGN KEY (cid_drop_off) REFERENCES containers(container_id),
		  FOREIGN KEY (cid_pick_up) REFERENCES containers(container_id)
		);''')
	cursor.execute(' PRAGMA forteign_keys=ON; ')
	connection.commit()




# ADD DATA TO THE TABLE
def add_data():
	global connection, cursor

	cursor.executescript('''''')
	connection.commit()




#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ACCOUNT MANAGER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# linkes account managers to the many options account managers have
#add the enter q to logout statement
def account_manager(username):
	global connection, cursor
	print()
	print("-------------------------------------------------------------")
	print("ACCOUNT MANAGER PAGE:")
	print("-------------------------------------------------------------")
	print( 'Welcome Account Manager ', username)

	print('What would you like to do?')
	while True:
		print ()
		print()
		print()
		options = input(' Enter 1 to view the customer information of all customers that you manage:\n Enter 2 to create a new customer account:\n Enter 3 to create a new service agreement for an existing customer:\n Enter 4 to view a customers summary: ')
		if options =='1':
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

	#print the customer information
	print(customer_info)
	print('\n\nWhat would you like to do?\n')
	option = input("Enter q to exist or h to return back to the homepage: ")

	if (option == 'q' or option == 'Q'):
		logout()
	elif (option == 'h' or option == 'H'):
		account_manager(username)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 2----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q2- user adds a new customer account to the database
def account_managerQ2(username):
	global connection, cursor
	#Create a new master account with all the required information. The manager of the account should be automatically set to the id of the account manager who is creating the account.
	#first we select the id of the account manager with the manager name equal to the login name
	t1 = (username,)
	cursor.execute('SELECT  m.pid,a.account_no FROM personnel p, account_managers m,accounts a WHERE p.pid = m.pid AND p.pid = a.account_mgr AND p.name = ?', (t1))
	info = cursor.fetchall()
	for i in info:
		#we now have the manager id
		mid = (i[0],)
		other_no = i[1]
		#grab new customer information from user 

		while True:
			account_no = input('ENTER AN ACCOUNT NUMBER(8 DIGITS): ')
			#make sure its len is 8 
			if len(account_no) != 8 or account_no == other_no:
				continue
			break


		#Get the start date
		while True:
			start_date= input("ENTER A START DATE (FORMAT YYYY-MM-DD): ")

			'''# GET THE YEAR
			date_list= date.split("-")  
			year=date_list[0]
			if len(year)!=4:
				print('L')
				continue
			# GET THE MONTH
			month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
			month=date_list[1]
			if month not in month_list:
				print('o')
				continue

			# GET THE DAY
			day=date_list[2]
			if day>31 or day<0:
				print('V')
				continue

			# Validate the date the user entered
			start_date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')
			if(datetime.datetime.now()<start_date):
				break

			else:
				print("TRY AGAIN (DATE HAS PASSED), ", end=" ")
				print('E')
				continue
			'''
			#return the date
			break


		
		while True:
			end_date = input("ENTER AN END DATE (FORMAT YYYY-MM-DD): ")
			break
		'''
			date_list= date.split("-")  
			if(len(date_list)!=3):
				print('L')
				continue

			# GET THE YEAR
			year=date_list[0]
			if len(year) != 4:
				print('o')
				continue

			# GET THE MONTH
			month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
			month=date_list[1]
			if month not in month_list:
				print('V')
				continue

			# GET THE DAY
			day=date_list[2]
			if day>31 and day<=0:
				print('E')
				continue


			#Check to make sure that the start date> todays date

			end_date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')

			if(datetime.datetime.now()>date):
				print("TRY AGAIN (DATE HAS PASSED), ", end=" ")
				continue
				'''
			

		#make sure customer name is not null
		while True:
			customer_name = input('ENTER A CUSTOMER NAME: ')
			if len(customer_name) == 0 or not customer_name.isalpha():
				continue
			break


		#make sure customer type is one of the types that we have
		while True:
			print('SELECT ONE OF THE FOLLOWING CUSTOMER TYPES:')
			print()
			print('1.COMMERCIALl\n2.INDUSTRIAL\n3.MUNICIPAL\n4.RESIDENTIAL')
			print()
			customer_type = input('ENTER 1,2,3,or 4: ')

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
				continue
			break

		#make contact info is correct fix in class
		while True:
			print()
			contact_info = input('ENTER CUSTOMER CONTACT INFO (FORMAT 000-000-0000): ')
			if valid_contact(contact_info) == False:
				continue
			break
			


		#make sure user enters a total amount
		while True:
			print()
			total_amount = input('Enter a total amount: ')
			if (len(total_amount)==0 or total_amount.isalpha()):
				continue
			break
		


		# now create a new customer account with the manager id
		cursor.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?);', (str(account_no,),str(mid),str(customer_name,),str(contact_info,),str(Type,),str(start_date,),str(end_date,),str(total_amount,)))
		connection.commit()
		print('...........')
		print('New Customer Account Created!\n')
		print




		#ask user if they want to add a service agreement to either an existing customer or a customer already int he database
		print('Would you like to create a service agreement for this customer?')
		print()
		#pause a bit
		create_sa = input('Enter Y for Yes or N for No: ')
		print()
		#if account manager does not want to add a service agreement to a new customer we ask if they would like to add one for any other customers they manage
		if (create_sa == 'N' or create_sa =='n'):
			print
			print('Would you like to create a service agreement for any other customers?')
			sa = input('Enter Y for Yes or N for No: ') 
			#if yes we add a service agreement to the another customer 
			if (sa == 'Y' or sa == 'y'):
				account_managerQ3(username);
			elif(sa == 'N' or sa =='n'):
				option = input('Enter q to logout or h to return back to homepage: ')
				if(option == 'H' or option == 'h'):
					account_manager(username)
				elif(option == 'q' or option == 'Q'):
					logout()
				

		#if user chooses to create a service agreement for the newly added customer
		elif (create_sa == 'Y' or create_sa =='y'):
			#select all the service numbers that we have 
			while True:
				location = input('Enter a location: ')
				if(location == 'q' or location == 'Q'):
					logout()
				elif len(location) < 3:
					continue
				break

			#check for valid waste type
			while True:
				print()
				print('SELECT ONE OF THE FOLLOWING')
				option = input('1.hazardous waste\n2.mixed waste\n3.construction waste\n4.metal\n5.compost\n6.paper\n7.plastic: ')
				if option == '1':
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
					continue


			#testcase for pickup schedule
			while True:
				print('SELECT FROM ONE OF THE FOLLOWING PICK UP SCHEDULES\n')
				print('1.Every Monday of every week\n2.Every Tuesday of every week\n3.Every Wednesday of every week\n4.Every Friday of every week\n5.Every Saturday of every week')

				pick_up_schedule = input('Enter a pick up schedule: ')

				if pick_up_schedule == '1':
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
					continue


			#testcase for local contact
			while True:
				print()
				local_contact = input('Enter a local contact: ')
				if valid_contact(local_contact)!= True:
					continue
				break

			#check for valid internal cost
			while True:
				print()
				internal_cost = input('Enter the internal cost: ')
				if (len(internal_cost)==0 or internal_cost.isalpha()):
					continue
				break

			#check for valid price
			while True:
				print()
				price = input('Enter a price: ')
				if (price == 'Q' or price == 'q'):
					logout
				elif (len(price) == 0 or price.isalpha()):
					continue
				break


				master_account = account_no

				#check if inputed customer info is valid 
				#randomly select a service number 
				service_no = random.randint(0,100)
				cursor.execute('SELECT service_no FROM service_agreements')
				badSA = cursor.fetchall()
				#if randomly selected service number is in use randomly select another one 
				for i in badSA:
					while (i == service_no):
						service_no = random.randint(0,100)

				#create the service agreement
				cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(master_account,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))

				time.sleep(0.2)
				print ('..........')
				print('\nService Agreement Created!')

			#user chooses to return to home or logout
			print()
			print()
			option = input("Enter q to exist or h to return back to the homepage: ")
			print()

			if (option == 'q' or option == 'Q'):
				logout()
			elif (option == 'h' or option == 'H'):
				account_manager(username)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 3----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q3-if user decides to create a service agreement for a customer that already exists 
def account_managerQ3(username):
	#First we get the manager id for the account manager
	t1 = (username,)
	cursor.execute('SELECT m.pid FROM personnel p, account_managers m WHERE p.pid = m.pid AND p.name = ?',(t1))
	#grab the list of manager pid 
	info = cursor.fetchall()
	i=(info[0])
	mid = i[0]
	#print all the custoemers an account manaager manages
	print("\nTHESE ARE ALL THE CUSTOMERS YOU MANAGE:")
	cursor.execute('SELECT a.customer_name,a.account_no  FROM accounts a, personnel p, account_managers m WHERE m.pid = p.pid and p.pid = a.account_mgr and p.pid = ?', (mid,))
	customer_info= cursor.fetchall()
	#select customer name
	customer_names = customer_info[0][0]
	#select customer number
	customer_nums = customer_info[0][1]
	print('Customer names: ',customer_names)
	print('Account number corresponding to the name ',customer_nums)


	while True:
		#then we get the customer who the account manager wants to make a service agreeement for
		customer_name = input('\nWhat is the name of the customer you want to make a servic agreement for?: ')
		customer_num = input('\nWhat is the account number of the customer: ')

		#check to see if customer_num is coorect
		if(customer_name != customer_names):
			print('Sorry you do not manage this customer')
			continue

		#see if the account num is the same as our selected account number
		elif (customer_num != customer_nums):
			print('incorrect customer account number')
			continue

		#check if user wantes to logout or return
		elif(customer_name == 'q' or customer_name == 'Q' or customer_num == 'q' or customer_num == 'Q'):
			logout()


		#check if account_number and customer name match up 
		cursor.execute('SELECT a.account_no from accounts a WHERE a.customer_name = ? and a.account_mgr = ? and a.account_no = ?',(customer_name,mid,customer_num))
		account_no= cursor.fetchall()

		if account_no[0][0] != customer_num:
			print('Incorecct account number or customer name')
			continue
		break
	
	#initialize account number as the enterd customer number
	a_no = customer_num 
	#account manager selects a customer they manage and we grab service agreement information
	#randomly select a service number 
	service_no = random.randint(0,100)
	cursor.execute('SELECT service_no FROM service_agreements')
	badSA = cursor.fetchall()
	#if randomly selected service number is in use randomly select another one 
	if badSA[0][:] == service_no:
		service_no.random.randint(0,100)


	#prompt user to enter values for service agreement
	else:
		#check for valid location
		while True:
			print()
			location = input('Enter a location: ')
			if(location == 'q' or location == 'Q'):
				logout()
			elif len(location) < 3:
				continue
			break

		#check for valid waste type
		while True:
			print()
			print('select from one of the following')
			option = input('1.hazardous waste\n2.mixed waste\n3.construction waste\n4.metal\n5.compost\n6.paper\n7.plastic: ')
			if option == '1':
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
				continue


		#testcase for pickup schedule
		while True:
			print()
			print('SELECT FROM ONE OF THE FOLLOWING PICK UP SCHEDULES\n')
			print('1.Every Monday of every week\n2.Every Tuesday of every week\n3.Every Wednesday of every week\n4.Every Friday of every week\n5.Every Saturday of every week')

			pick_up_schedule = input('Enter a pick up schedule: ')

			if pick_up_schedule == '1':
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
				continue
		#testcase for local contact
		while True:
			print()
			local_contact = input('Enter a local contact: ')
			if valid_contact(local_contact)!= True:
				continue
			break

		#check for valid internal cost
		while True:
			print()
			internal_cost = input('Enter the internal cost: ')
			if (len(internal_cost)==0 or internal_cost.isalpha()):
				continue
			break

		#check for valid price
		while True:
			print()
			price = input('Enter a price: ')
			if (price == 'Q' or price == 'q'):
				logout
			elif (len(price) == 0 or price.isalpha()):
				continue
			break


		#if the information is valid then we create a service agreement account for this customer
		cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(a_no,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))
		time.sleep(0.2)
		print ('..........')
		print('\nService Agreement Created!')

		#allow user the option to continuw or logout
		print
		option = input("Enter q to exist or h to return back to the homepage")

		if (option == 'q' or option == 'Q'):
			logout()
		elif (option == 'h' or option == 'H'):
			account_manager(username)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------QUESTION 4----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Q4 prints the summary for a single  customer					
def account_managerQ4(username):
	#first we select the manager id 
	t1 = (username,)
	cursor.execute('SELECT m.pid FROM personnel p, account_managers m WHERE p.pid = m.pid AND p.name = ?',(t1))
	
	#grab the list of manager pid 
	info = cursor.fetchall()
	i=(info[0])
	mid = i[0]

	#Then we grab the customer information
	print("THESE ARE ALL THE CUSTOMERS YOU MANAGE\n")
	cursor.execute('SELECT a.customer_name,a.account_no FROM accounts a WHERE a.account_mgr = ?', (mid,))
	customer_info = cursor.fetchall()
	customer_names = customer_info[0][0]
	account_nos = customer_info[0][1]
	

	while True:
		print('Customer names: ' ,customer_names)
		print('Account numbers: ',account_nos)
		#as user to enter customer name
		print
		customer_name = input('\nWhat is the name of the customer who you want to see a summary report for?: ')
		customer_no = input('\nWhat is the account number of the customer who you want to see a summary report for?: ')

		#grab the account number if user input is valid
		cursor.execute('SELECT a.account_no from accounts a WHERE a.customer_name = ? and a.account_mgr = ? and a.account_no = ?',(customer_name,mid,customer_no))
		account_no= cursor.fetchall()

		if str(customer_names[0][0]) == customer_name:
			continue
		elif account_no == []:
			print
			print('Incorecct account number or customer name\n')
			continue
		break


	account_no = (customer_no)
	#select the count of services, sum of internal cost, sum of prices, and the count of the different waste types
	cursor.execute('SELECT COUNT(s.service_no), SUM(s.internal_cost),SUM(s.price) FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = a.account_no AND a.customer_name =? AND a.account_no =?' ,(customer_name,account_no))
	connection.commit()
	summary = cursor.fetchall()
	

	cursor.execute('SELECT COUNT(*)  FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = ? AND a.customer_name = ? GROUP BY s.waste_type' ,(account_no,customer_name))
	connection.commit()
	waste_types = cursor.fetchall()

	#print the summary for the user and the number of distinct waste_types
	distinct_types = len(waste_types)
	summarys = []
	summarys.append(summary[0][:])
	summarys.append(distinct_types)

	print('Summary: ',summarys)
	#user chooses to return to account manager page or logout

	option = input("\n\nEnter q to exist or h to return back to the homepage: ")

	if (option == 'q' or option == 'Q'):
		logout()
	elif (option == 'h' or option == 'H'):
		account_manager(username)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------






#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------SUPERVISOR FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Supervisor(username):
	print("Welcome Supervisor!\n")
	global cursor, connection
	cursor.execute('''SELECT user_id FROM users where login = ?''', (username,))
	connection.commit()
	supervisor_pid = cursor.fetchone()
	while True:
	    print("Enter q to exit")
	    print("Enter m to create a new master account")
	    print("Enter s for a summary report for single customer")
	    decision = input("Enter a for account manager summary report")
	    if decision == 'm' or decision == 'M':
	        create_master_account()
	        break
	    if decision == 's' or decision == 'S':
	        summary_customer()
	        break
	    if decision == 'a' or decision == 'A':
	        summary_account_manager(supervisor_pid)
	        break
	    else
	        logout()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------Question 1----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def create_master_account(username):
    global connection, cursor
    while True:
        account_no = input("Enter an account number: ")
        if len(account_no) == 8:
            break
    while True:
        manager = input("Select the account manager's PID:")
        cursor.execute('''Select *
                            FROM account_manager
                            WHERE pid = ?''', (manager,))
        exists = cursor.fetchall()
        if exists != []:
            break

    while True:
        start_date=input("Enter the start date: ")
    while True:
        end_date=input("Enter the end date: ")
    customer_name=input("Enter the customer name: ")
    contact_info=input("Enter the contact info: ")
    customer_type=input("Enter the customer type: ")
    total_amount=input("Enter the total amount: ")

    cusor.execute('INSERT INTO account VALUES(?,?,?,?,?,?,?,?)', (account_no, manager, customer_name, contact_info, customer_type, start_date, total_amount))
    connection.commit()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------Question 2-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def summary_customer(supervisor_pid):
    global cursor, connection
    cusor.execute('''SELECT p.name FROM personnel p, account_managers a WHERE a.pid = p.pid AND p.supervisor_pid = ?''', (supervisor_pid,))
    managers = cursor.fetchall()
    connection.commit()
    print("AVAILABLE MANAGERS:\n")
    print("--"*80)
    for i in managers:
        print(i)
    print("--"*80)
    while True:
        manager_selection = input("PLEASE SELECT ONE OF THE MANAGERS:")
        cursor.execute('''SELECT p.name
        FROM account_managers a, personnel p
        WHERE a.pid = p.pid
        AND p.supervisor_pid = ?
        AND p.name = ?''', (supervisor_pid,manager_selection))
        chosen_manager = cursor.fetchall()
        connection.commit()
        if len(chosen_manager) >= 2:
            while True:
                cursor.execute('''SELECT p.pid
                                FROM account_managers a, personnel p
                                WHERE a.pid = p.pid
                                AND p.supervisor_pid = ?
                                AND p.name = ?''', (supervisor_pid, manager_selection))
                duplicate_managers = cursor.fetchall()
                connection.commit()
                print("DUPLICATE MANAGER PLEASE SPECIFY PERSONNEL ID FROM BELOW:")
                print("--"*80)
                for i in duplicate_managers:
                        print(i)
                print("--"*80)
                chosen_pid = input("SELECT MANAGER PID:")
                check_pid = cursor.execute('''SELECT p.pid
                                                    FROM accounts a, personnel p
                                                    WHERE a.account_mgr = p.pid
                                                    AND p.supervisor_pid = ?
                                                    AND p.pid = ?
                                                    AND p.name = ?''',(supervisor_pid,chosen_pid, chosen_manager))
                if check_pid != []
                    manager_selection = chosen_pid
                    break
                break
        if chosen_manager != []:
            cursor.execute('''SELECT p.pid
            FROM personnel p, account_managers a
            WHERE  a.pid = p.pid
            AND p.name = ?
            AND p.supervisor_pid = ?''', (manager_selection, supervisor_pid))
            manager_selection = cursor.fetchone()
            connection.commit()
            break

        print("AVAILABLE MANAGERS:\n")
        print("--"*80)
        for i in managers:
            print(i)
        print("--"*80)
        print("\n")

    print("AVAILABLE CUSTOMERS:\n")
    print("--"*80)
    cursor.execute('''SELECT customer_name FROM accounts WHERE account_mgr = ?''', (chosen_manager,))
    available_customers = cursor.fetchall()
    connection.commit()
    for i in available_customers:
        print(i)
    print("--"*80)
    print("\n")

    while True:
        customer_selection = input("PLEASE SELECT ONE OF THE CUSTOMERS: ")
        cursor.execute('''SELECT customer_name FROM accounts WHERE account_mgr = ?''', (manager_selection,))
        chosen_customer = cursor.fetchall()
        connection.commit()
        if len(chosen_customer) >= 2:
            while True:
                cursor.execute('''SELECT account_no
                FROM accounts
                WHERE customer_name = ?
                AND account_mgr = ?''', (customer_selection,manager_selection))
                account_numbers = cursor.fetchall()
                connection.commit()
                print("DUPLICATE CUSTOMER NAMES CHOOSE ACCOUNT NUMBER FROM BELOW\n")
                print("--"*80)
                for i in account_numbers:
                    print(i)
                print("--"*80)
                account_chosen = input("PLEASE ENTER ACCOUNT NUMBER:")
                cursor.execute('''SELECT account_no
                FROM accounts a
                WHERE customer_name = ?
                AND account_mgr = ?
                AND account_no = ?''', (customer_selection,manager_selection,account_chosen))
                customer_account = cursor.fetchone()
                if customer_account != []:
                    break
                break
        if chosen_customer != []
            cursor.execute('''SELECT a.account_no
            FROM accounts a
            WHERE m.account_mgr = ?
            AND a.customer_name = ?''', (manager_selection, customer_selection))
            customer_account = cursor.fetchone()
            connection.commit()
            break
        for i in available_customers:
            print(i)
        print("--"*80)
        print("\n")

    cursor.execute('''SELECT count(s.service_no), sum(s.price), sum(s.internal_cost)
                    FROM service_agreements s
                    WHERE s.master_account = ?
                    GROUP BY s.waste_type''', (customer_account,))
                    summary = cursor.fetchall()
                    connection.commit()

                    cursor.execute('''SELECT count(*)
                    FROM service_agreements s
                    WHERE s.master_account = ?
                    GROUP BY s.waste_type''', (customer_account,))
                    waste_types = cursor.fetchall()
                    connection.commit()
                    number_types = len(waste_types)

                    for i in summary:
                        print(i)
                    print(number_types)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------Question 3----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


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
def driver():
	global connection, cursor

	print("\n"*40)
	print("-------------------------------------------------------------")
	print("WELCOME DRIVER!!")
	print("-------------------------------------------------------------")
	print('Enter q to exit!')

	print("\n\n")

	#Get the start date
	while True:
		start_date= input("ENTER START DATE (FORMAT YYYY-MM-DD): ")
		if (start_date=="q" or start_date=="Q"):
				logout()

		# GET THE YEAR
		date_list= start_date.split("-")  
		year=date_list[0]
		if len(year)==4:

			break
		else:
			continue

		# GET THE MONTH
		month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
		month=date_list[1]
		if month in month_list:
			break
		else:
			continue
	
		# GET THE DAY
		day=date_list[2]
		if day<=31 and day>0:
			break
		else:
			continue


	#Get the end date
	while True:
		end_date= input("ENTER END DATE (FORMAT YYYY-MM-DD): ")

		if (end_date=="q" or end_date=="Q"):
				logout()

		# GET THE YEAR
		date_list= end_date.split("-")  
		year=date_list[0]
		if len(year)==4:
			break
		else:
			continue

		# GET THE MONTH
		month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
		month=date_list[1]
		if month in month_list:
			break
		else:
			continue
	
		# GET THE DAY
		day=date_list[2]
		if day<=31 and day>0:
			break
		else:
			continue

	t=(start_date, end_date)
	cursor.execute('''
		SELECT sa.location, sa.local_contact, sa.waste_type, s.cid_drop_off, s.cid_pick_up  
		from service_agreements sa, service_fulfillments s
		where sa.master_account=s.master_account
		and s.service_no=sa.service_no
		and s.date_time>=? 
		and s.date_time=<?''', t)
	connection.commit()
	rows=cursor.fetchall()

	# Display Tours formatted
	print()
	print()
	print("INFORMATION ABOUT THE TOUR CONSISTS OF THE FOLLOWING: ")
	values=["LOCATION", "LOCAL CONTACT", "WASTE TYPE", "DROP OFF CONTAINER ID ", "PICK UP CONTAINER ID"]
	string="%10s|%10s|%10s|%10s|%10s"%(values[0].ljust(20), values[1].ljust(20), values[2].ljust(20), values[3].ljust(20), values[4].ljust(40))
	print(string)
	print("--"*80)
	service_no_list=[]

	for value in rows:
		value=list(value)
		service_no_list.append(value[0])
		formatted_string="%10s|%10s|%10s|%10s|%10s" %(value[0].ljust(20), value[1].ljust(20), value[2].ljust(20), value[3].ljust(20), value[4].ljust(40))
		print(formatted_string)
		print()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------









#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------DISPATCHER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dispatcher():
	global connection, cursor

	print("\n"*40)
	print("-------------------------------------------------------------")
	print("WELCOME DISPATCHER!!")
	print("-------------------------------------------------------------")
	print('Enter q to exit!')

	print("\n\n")

	# Select a service_agreement, driver, truck, and a container to be dropped off and picked up
	
	# Select a service no for a particular service agreement
	service_no= Dispatcher_getService_no()

	# Find master account
	cursor.execute('''
		select s.master_account
		from service agreements s
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
	print()
	print()

	# Set the date
	date=setDate()

	# Create entries in the table service_fulfillments for upcoming days
	add_service_fulliment(date, master_account, service_no, truck, driver, cid_drop_off, cid_pick_up)



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
	print()
	print("SELECT ONE SERVICE NO FROM THE FOLLOWING SERVICE AGREEMENTS:")
	
	values=["SERVICE NO", "MASTER ACCOUNT", "LOCATION", "WASTE TYPE",  "PICK UP SCHEDULE",  "LOCAL CONTACT", "INTERNAL COST",  "PRICE"]
	string="%10s|%10s|%10s|%10s|%10s|%10s|%10s|%10s"%(values[0].ljust(20), values[1].ljust(20), values[2].ljust(20), values[3].ljust(20), values[4].ljust(40), values[5].ljust(20), values[6].ljust(20), values[7].ljust(20))
	print(string)
	print("--"*80)

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
			continue
		else:
			break

	# Return the service no choosen from the dispatcher
	return service_no

# Select the driver to fulfill a task
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
	print()
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
			
		print()
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
	print()
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

	date_array=[]
	print("ENTER DATE (FORMAT YYYY-MM-DD): ")

	date_list=[]

	while True:

		while True:
			date= input("ENTER DATE (FORMAT YYYY-MM-DD): ")
			if (date=="q" or date=="Q"):
				logout()
			# GET THE YEAR
			date_list= date.split("-")  
			year=date_list[0]
			if len(year)==4:

				break
			else:
				continue

			# GET THE MONTH
			month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
			month=date_list[1]
			if month in month_list:
				break
			else:
				continue
		
			# GET THE DAY
			day=date_list[2]
			if day<=31 and day>0:
				break
			else:
				continue

		# Validate the date the user entered
		date= datetime.datetime.strptime(date_list[0]+'-'+date_list[1]+'-'+date_list[2], '%Y-%m-%d')

		if(datetime.datetime.now()<date):
			break
		else:
			print("TRY AGAIN (DATE HAS PASSED), ", end=" ")
			continue

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
		supervisor(username)

			
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
		print('Enter q to exit when Prompted to enter data!!!')
		role = find_role(username)
		print(role)
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
	print("\n"*40)
	print("-------------------------------------------------------------")
	print("LOGIN PAGE:")
	print("-------------------------------------------------------------")
	print('Enter q to exit!')

	count=0
	while count<3:
		print("ATTEMPTS REMAINING: %d" % (3-count) )
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
		time.sleep(0.3)

		# If hashed password is the same as the hashed database password then login is successful
		status = Authenticate(psw,username)
		# If Login is not successful, loop back to login
		if not status:
			print("Username and Password do not match\n\n")
			count=count+1
		# If the user successfully logged in we find its roles
		if status:
			start(username)

			
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

	print("\n"*40)
	print("-------------------------------------------------------------")
	print("CREATE ACCOUNT PAGE:")
	print("-------------------------------------------------------------")
	print('Enter q to exit!')

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
	print()
	print("Goodbye!")
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
	# Call to the Create Table Function
	create_tables()
	# Loop to login to the system 
	add_data()


	print("\n"*40)
	print("Welcome!")
	decision= input('PRESS L TO LOGIN IN, OR PRESS C TO CREATE AN ACCOUNT: ')
	
	if decision == 'C' or decision== 'c':
			create_account()
	
	elif decision == 'L' or  decision=='l':
		login()

	print()
	print()
	print("GoodBye")
	
main()
	


