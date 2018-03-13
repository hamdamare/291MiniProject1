# WORK DONE BY AYUB AHMED, HAMDA MARE, AND HAMSE MARE

# Citations:

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

	#Add data to tables

	# Pid: DRIVERS: 			11111 - 12222
	# Pid: Account Managers: 	13333 - 14444
	# Pid: Dispatchers: 		15555 - 16666
	# Pid: Supervisors: 		17777 - 18888

	cursor.executescript('''

		INSERT INTO trucks VALUES('222','Ford F-Series','roll-off');

		--trucks owned by drivers
		INSERT INTO trucks VALUES('333','Honda Ridgeline','garbage bin collector');
		INSERT INTO trucks VALUES('2333','Cadillac Escalade EXT','front loader');
		INSERT INTO trucks VALUES('2444','Chevrolet Colorado','garbage bin collector');
		
		--ACCOUNT MANAGER
		INSERT INTO account_managers VALUES('13333','small accounts manager','8th Street South');
		INSERT INTO account_managers VALUES('14444','major accounts manager','Main Street West');

		--ACCOUNTS
		INSERT INTO accounts VALUES('87625036','13333','Rhianna Wilkinson','(201) 874-4399','residential','2006-05-19 13:16:14','2018-02-12 06:50:29',837646.52);
		INSERT INTO accounts VALUES('73833854','14444','Reese Thornton','(745) 516-3060','commercial','2004-01-18 03:26:06','2013-02-09 15:56:27',893618.73);
		INSERT INTO accounts VALUES('34910788','13333','Jarrett Castro','(883) 338-6912','commercial','2007-01-28 20:29:51','2019-11-06 10:14:50',658737.09);
		INSERT INTO accounts VALUES('12029871','14444','Areli Lowery','(706) 692-2734','industrial','2000-08-03 20:48:36','2018-03-07 04:15:21',322370.9);
		INSERT INTO accounts VALUES('85043375','13333','Lilyana Gaines','(425) 810-3987','municipal','2003-04-02 7:38:38','2016-02-10 21:45:17',111695.11);
		INSERT INTO accounts VALUES('72149574','14444','Lila Sloan','(626) 284-7432','industrial','2002-11-15 12:31:42','2018-04-04 02:55:07',767403.0);
		INSERT INTO accounts VALUES('23593363','13333','Alonzo Shea','(496) 102-3035','commercial','2006-07-25 10:39:12','2019-07-22 16:51:29',428144.53);

		--Service agreements
		INSERT INTO service_agreements VALUES('1','87625036','Elm Avenue','hazardous waste','every Tuesday of every week','(904) 694-9532',566.45,1994);
		INSERT INTO service_agreements VALUES('2','73833854','Essex Court','mixed waste','every Wednesday of every week','(947) 900-1946',657.8,1643);
		INSERT INTO service_agreements VALUES('3','34910788','Circle Drive','construction waste','every Monday of every week','(149) 953-8810',360.87,1225);
		INSERT INTO service_agreements VALUES('4','12029871','Delaware Avenue','hazardous waste','every Friday of every week','(306) 162-4684',464.2,1609);
		INSERT INTO service_agreements VALUES('5','85043375','Atlantic Avenue','metal','every Saturday of every week','(923) 798-0938',412.44,2601);

		--Personnel
		INSERT INTO personnel VALUES('11111','Dan','matloff@sbcglobal.net','Windsor Drive','17777');
		INSERT INTO personnel VALUES('12222','Charlotte','mjewell@optonline.net','Maple Avenue','18888');
		INSERT INTO personnel VALUES('13333','Grady','panolex@sbcglobal.net','Hillcrest Avenue','18888');
		INSERT INTO personnel VALUES('14444','Carina','phyruxus@me.com','Schoolhouse Lane','17777');
		INSERT INTO personnel VALUES('15555','Cameron','harryh@icloud.com','Cambridge Court','18888');
		INSERT INTO personnel VALUES('16666','Dan','matloff@sbcglobal.net','Windsor Drive','17777');
		INSERT INTO personnel VALUES('17777','Charlotte','mjewell@optonline.net','Maple Avenue','18888');
		INSERT INTO personnel VALUES('18888','Grady','panolex@sbcglobal.net','Hillcrest Avenue','17777');

		--maintenance_records of drivers owned trucks
		INSERT INTO maintenance_records VALUES('222','2011-08-30 19:19:46','Inspection');

		--maintenance_records of drivers company trucks
		INSERT INTO maintenance_records VALUES('333','2011-08-30 19:19:46','Inspection');


		--Dummy containers
		INSERT INTO containers VALUES('0000','Dummy Container','2015-03-10 20:42:44');
		INSERT INTO containers VALUES('1','Auger Compactor','2015-03-10 20:42:44');
		INSERT INTO containers VALUES('2','Roll-Off dumpster','2009-10-24 02:53:48');
		INSERT INTO containers VALUES('3','Closed-Topped','2016-12-10 06:14:33');
		INSERT INTO containers VALUES('4','Open-Topped','2012-04-23 09:35:36');
		INSERT INTO containers VALUES('5','Hydraulic Compactor','2015-03-10 20:42:44');
		INSERT INTO containers VALUES('6','Roll-Off dumpster','2009-10-24 02:53:48');
		INSERT INTO containers VALUES('7','Open-Topped','2016-12-10 06:14:33');
		INSERT INTO containers VALUES('8','Closed-Topped','2012-04-23 09:35:36');
		INSERT INTO containers VALUES('9','Auger Compactor','2016-12-10 06:14:33');
		INSERT INTO containers VALUES('10','Hydraulic Compactor','2012-04-23 09:35:36');


		INSERT INTO waste_types VALUES('plastic');
		INSERT INTO waste_types VALUES('paper');
		INSERT INTO waste_types VALUES('hazardous waste');
		INSERT INTO waste_types VALUES('construction waste');
		INSERT INTO waste_types VALUES('mixed waste');
		INSERT INTO waste_types VALUES('metal');
		INSERT INTO waste_types VALUES('compost');


		INSERT INTO container_waste_types VALUES('1','mixed waste');
		INSERT INTO container_waste_types VALUES('2','paper');
		INSERT INTO container_waste_types VALUES('3','mixed waste');
		INSERT INTO container_waste_types VALUES('4','construction waste');
		INSERT INTO container_waste_types VALUES('5','hazardous waste');
		INSERT INTO container_waste_types VALUES('6','compost');
		INSERT INTO container_waste_types VALUES('7','construction waste');
		INSERT INTO container_waste_types VALUES('8','hazardous waste');
		INSERT INTO container_waste_types VALUES('9','plastic');
		INSERT INTO container_waste_types VALUES('10','hazardous waste');

		--drivers who own a truck
		INSERT INTO drivers VALUES('11111','Single Trailer','222');
		--drivers who do not own a truck
		INSERT INTO drivers VALUES('12222','HAZMAT',NULL);


		INSERT INTO service_fulfillments VALUES('2018-07-30 03:47:43','87625036','1','2111','11111','1','0000');

		INSERT INTO service_fulfillments VALUES('2019-07-30 03:47:43','73833854','2', '2111','11111','2','1');

		INSERT INTO service_fulfillments VALUES('2020-07-30 03:47:43','34910788','3','2111','11111','3','0000');

		INSERT INTO service_fulfillments VALUES('2022-07-30 03:47:43','12029871','4','2111','11111','3','4');

		INSERT INTO service_fulfillments VALUES('2023-07-30 03:47:43','85043375','5','2111','11111','4','3');''')

	connection.commit()

	

	a=encrypt_password("2")
	b=encrypt_password("4")
	c=encrypt_password("6")
	d=encrypt_password("8")

	cursor.execute('''
		INSERT INTO users VALUES('12222','driver','1',?)''', (a,))
	connection.commit()

	cursor.execute('''
		INSERT INTO users VALUES('14444','account manager','2',?)''', (b,))
	connection.commit()

	cursor.execute('''
		INSERT INTO users VALUES('16666','dispatcher','3',?)''', (c,))
	connection.commit()

	cursor.execute('''
		INSERT INTO users VALUES('18888','supervisor','4',?)''', (d,))
	connection.commit()



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ACCOUNT MANAGER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# linkes account managers to the many options account managers have
#add the enter q to logout statement
def account_manager(username):
	global connection, cursor
	print("\n"*40)
	print("-------------------------------------------------------------")
	print("WELCOME ACCOUNT MANAGER!")
	print("-------------------------------------------------------------")
	print('Enter q to exit!')

	print('What would you like to do?')
	options = input(' Enter 1 to view the customer information of all customers that you manage:\n Enter 2 to create a new customer account:\n Enter 3 to create a new service agreement for an existing customer:\n Enter 4 to view a customers summary: ')
	while True:
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
	print(customer_info)

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
	print(info)
	for i in info:
		#we now have the manager id
		mid = (i[0],)
		other_no = i[1]
		print(mid)
		print(other_no)
		#grab new customer information from user 

		while True:
			account_no = input('ENTER AN ACCOUNT NUMBER(8 DIGITS): ')
			#make sure its len is 8 
			if len(account_no) != 8 or account_no == other_no:
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
		if day>31 and day<=0:
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
		if day>31 and day<=0:
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
		if len(customer_name) == 0:
			continue
		break


	#make sure customer type is one of the types that we have
	while True:
		print('SELECT ONE OF THE FOLLOWING CUSTOMER TYPES:')
		print
		print('1.COMMERCIALl\n2.INDUSTRIAL\n3.MUNICIPAL\n4.RESIDENTIAL')
		print
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
		contact_info = input('ENTER CUSTOMER CONTACT INFO (FORMAT 000-000-0000): ')
		#ohone_list 
		phone_list=['0','1','2','3','4','5','6','7','8','9','10','11','12']
		if len(contact_info) != 12:
				continue
		break

	#make sure user enters a total amount
	while True:
		total_amount = input('Enter a total amount: ')
		if len(total_amount)==0:
			continue
		break
	
	# now create a new customer account with the manager id
	cursor.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?);', (str(account_no,),str(mid),str(customer_name,),str(contact_info,),str(Type,),str(start_date,),str(end_date,),str(total_amount,)))
	connection.commit()
	time.sleep(0.2)
	print('.....')
	print('Created a new customer account!\n')
	print

	#ask user if they want to add a service agreement to either an existing customer or a customer already int he database
	print('Would you like to create a service agreement for this customer?')
	create_sa = input('Enter Y for Yes or N for No: ')
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
		location = input('Enter a location: ')
		waste_type = input('Enter a waste_type: ')
		pick_up_schedule = input('Enter a pick up schedule: ')
		local_contact = input('Enter a local contact: ')
		internal_cost = input('Enter the internal cost: ')
		price = input('Enter a price: ')
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
				return service_no

		#create the service agreement
		cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(master_account,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))

		time.sleep(0.2)
		print ('..........')
		print('\nService Agreement Created!')

		#user chooses to return to home or logout
		print
		print
		option = input("Enter q to exist or h to return back to the homepage")

		if (option == 'q' or option == 'Q'):
			logout()
		elif (option == 'h' or option == 'H'):
			account_manager()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
	print("\nThese are all the customers you manage:")
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

		elif (customer_num != customer_nums):
			print('inccorect customer account number')
			continue
		elif(customer_name == 'q' or customer_name == 'Q' or customer_num == 'q' or customer_num == 'Q'):
			logout()
		#check if account_number and customer name match up 
		print(mid)
		print(customer_name)
		print(customer_num)
		cursor.execute('SELECT a.account_no from accounts a WHERE a.customer_name = ? and a.account_mgr = ? and a.account_no = ?',(customer_name,mid,customer_num))
		account_no= cursor.fetchall()
		print(account_no)

		if account_no[0][0] != customer_num:
			print('Inccorecct account number or customer name')
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
		print(badSA[0][:] )
		service_no.random.randint(0,100)
		print(service_no)

	
	else:
		#prompt user to enter values for a service agreement 
		while True:
			location = input('Enter a location: ')
			if(location == 'q' or location == 'Q'):
				logout()
			elif len(location) == 0:
				continue
			break

		while True:
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
		pick_up_schedule = input('Enter a pick up schedule: ')
		#testcase for local contact
		local_contact = input('Enter a local contact: ')

		while True:
			internal_cost = input('Enter the internal cost: ')
			if len(internal_cost)==0:
				continue
			break

		while True:
			price = input('Enter a price: ')
			if (price == 'Q' or price == 'q'):
				logout
			elif len(price) == 0:
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
			account_manager()

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
	print("These are all the customers you manage\n")
	cursor.execute('SELECT a.customer_name,a.account_no FROM accounts a WHERE a.account_mgr = ?', (mid,))
	customer_info = cursor.fetchall()
	customer_names = customer_info[0][0]
	account_nos = customer_info[0][1]
	print(customer_names)
	print(account_nos)

	while True:
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
			print('Incorrect account number or customer name')
			continue
		break


	account_no = (customer_no)
	print(account_no)
	#select the count of services, sum of internal cost, sum of prices, and the count of the different waste types
	cursor.execute('SELECT COUNT(s.service_no), SUM(s.internal_cost),SUM(s.price) FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = a.account_no AND a.customer_name =? AND a.account_no =?' ,(customer_name,account_no))
	connection.commit()
	summary = cursor.fetchall()
	

	cursor.execute('SELECT COUNT(*)  FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = ? AND a.customer_name = ? GROUP BY s.waste_type' ,(account_no,customer_name))
	connection.commit()
	waste_types = cursor.fetchall()


	#print the summary for the user and the number of distinct waste_types
	print(summary)
	distinct_types = len(waste_types)
	print(distinct_types)

	#user chooses to return to account manager page or logout
	print
	print
	option = input("Enter q to exist or h to return back to the homepage")

	if (option == 'q' or option == 'Q'):
		logout()
	elif (option == 'h' or option == 'H'):
		account_manager()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------







#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------SUPERVISOR FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Supervisor(username):
	global cursor, connection

	print("\n"*40)
	print("-------------------------------------------------------------")
	print("Welcome Supervisor!\n")
	print("-------------------------------------------------------------")
	print('Enter q to exit!')

	##Get the user_id of the logged in supervisor
	cursor.execute('''SELECT user_id FROM users where login = ?''', (username,))
	supervisor_pid = cursor.fetchone()
	connection.commit()

	#Allow the user to choose from a range of 3 options or press q to exit
	while True:
	    print("Enter m: Create a new master account")
	    print("Enter s:  Summary report for single customer")
	    print("Enter a:  Summary of account managers")
	    decision = input("Enter a for account manager summary report")

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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------Question 1----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#This function creates a new master account with one of the account managers under the supervisor
def create_master_account(supervisor_pid):
    global connection, cursor

    while True:
        print("AVAILABLE MANAGER PID")
        print("--"*80)
        cursor.execute('''SELECT m.pid
                         FROM personnel p, account_manager m
                         WHERE m.pid = p.pid
                         p.supervisor_pid = ?''', (supervisor_pid,))
        available_managers = cursor.fetchall()
        connection.commit()
        for i in available_managers:
            print(i)
        print("--"*80)
        manager = input("ENTER MANAGER PID:")
        cursor.execute('''SELECT p.pid
                            FROM account_manager a, personnel p
                            WHERE p.pid = a.pid
                            AND p.pid = ?
                            AND p.supervisor_pid = ?''', (manager, supervisor_pid))
        exists = cursor.fetchall()
        connection.commit()
        if exists != []:
            break

    while True:
        account_number = input("Enter an account number of length 8: ")
        #account number must be a length of 8
        cursor.execute('''SELECT account_no
                            FROM accounts a
                            WHERE account_no = ?''', (account_number,))
        account_exists = cursor.fetchall()
        connection.commit()
        if account_exists != []:
            break
        print("That account number has already been taken please try again")
        

    start_date=input("Enter the start date: ")
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
                if check_pid != []:
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
        if chosen_customer != []:
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
#---------------------------------------------------QUESTION 3--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def summary_account_manager(supervisor_pid):
    global connection, cursor
    cursor.execute('''
    	SELECT count(master_account), count(service_no), sum(price), sum(internal_cost)
	    FROM service_agreements s, personnel p, accounts ac
	    WHERE p.supervisor_pid = ? AND p.pid = ac.account_mgr AND ac.account_no = s.master_account
	    GROUP BY p.pid
	    ORDER BY (sum(price)-sum(internal_cost))''', (supervisor_pid,))
    row = c.fetchall()
    connection.commit()
    print("MANAGER ACCOUNT SUMMARY\n")
    print("--"*80)
    values = ["NUMBER OF MASTER AGREEMENTS", "NUMBER OF SERVICE AGREEMENTS", "TOTAL PRICE", "TOTAL COST"]
    string ="%10s|%10s|%.2f|%.2f"%(values[0].ljust(20), values[1].ljust(20), values[2], values[3])
    print(string)
    print("--"*80)
    summary_manager = []
    for i in rows:
        i = list(i)
        summary_manager.append(value[0])
        format_string = "%10s|%10s|%.2f|%.2f"%(values[0].ljust(20), values[1].ljust(20), values[2], values[3])
        print(format_string)
        print()
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
		if day>31 and day<=0:
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
		if day>31 and day<=0:
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
		if day>31 and day<=0:
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
	# Call to the Create Table Function
	create_tables()
	# Loop to login to the system 
	add_data()

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
	


