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
logout=False



# ADD DATA TO THE TABLE
def add_data():
	global connection, cursor


	cursor.executescript(
		'''	
		INSERT INTO trucks VALUES('1111','Ford F-Series','roll-off');
		INSERT INTO trucks VALUES('1222','Honda Ridgeline','garbage bin collector');
		INSERT INTO trucks VALUES('1333','Cadillac Escalade EXT','front loader');
		INSERT INTO trucks VALUES('1444','Chevrolet Colorado','garbage bin collector');

		--trucks owned by drivers
		INSERT INTO trucks VALUES('2111','Ford F-Series','roll-off');
		INSERT INTO trucks VALUES('2222','Honda Ridgeline','garbage bin collector');
		INSERT INTO trucks VALUES('2333','Cadillac Escalade EXT','front loader');
		INSERT INTO trucks VALUES('2444','Chevrolet Colorado','garbage bin collector');


		INSERT INTO account_managers VALUES('34725','small accounts manager','8th Street South');
		INSERT INTO account_managers VALUES('42134','major accounts manager','Main Street West');


		--Users 
		INSERT INTO users VALUES('34725','dispatcher','Dan','pass1');
		INSERT INTO users VALUES('42134','account manager','Charlotte','pass2');
		INSERT INTO users VALUES('16830','account manager','Grady','pass3');
		INSERT INTO users VALUES('73709','account manager','Carina','pass4');
		INSERT INTO users VALUES('15625','account manager','Cameron','pass5');
		INSERT INTO users VALUES('56468','account manager','Roderick','pass6');
		INSERT INTO users VALUES('81480','account manager','Katrina','pass7');
		INSERT INTO users VALUES('48660','account manager','Jeremy','pass8');


		--Accounts
		INSERT INTO accounts VALUES('87625036','34725','Rhianna Wilkinson','(201) 874-4399','residential','2006-05-19 13:16:14','2018-02-12 06:50:29',837646.52);
		INSERT INTO accounts VALUES('73833854','42134','Reese Thornton','(745) 516-3060','commercial','2004-01-18 03:26:06','2013-02-09 15:56:27',893618.73);
		INSERT INTO accounts VALUES('34910788','16830','Jarrett Castro','(883) 338-6912','commercial','2007-01-28 20:29:51','2019-11-06 10:14:50',658737.09);
		INSERT INTO accounts VALUES('12029871','73709','Areli Lowery','(706) 692-2734','industrial','2000-08-03 20:48:36','2018-03-07 04:15:21',322370.9);
		INSERT INTO accounts VALUES('85043375','15625','Lilyana Gaines','(425) 810-3987','municipal','2003-04-02 7:38:38','2016-02-10 21:45:17',111695.11);
		INSERT INTO accounts VALUES('72149574','56468','Lila Sloan','(626) 284-7432','industrial','2002-11-15 12:31:42','2018-04-04 02:55:07',767403.0);
		INSERT INTO accounts VALUES('23593363','34725','Alonzo Shea','(496) 102-3035','commercial','2006-07-25 10:39:12','2019-07-22 16:51:29',428144.53);


		--Service agreements

		INSERT INTO service_agreements VALUES('1','87625036','Elm Avenue','hazardous waste','every Tuesday of every week','(904) 694-9532',566.45,1994);
		INSERT INTO service_agreements VALUES('2','73833854','Essex Court','mixed waste','every Wednesday of every week','(947) 900-1946',657.8,1643);
		INSERT INTO service_agreements VALUES('3','34910788','Circle Drive','construction waste','every Monday of every week','(149) 953-8810',360.87,1225);
		INSERT INTO service_agreements VALUES('4','12029871','Delaware Avenue','hazardous waste','every Friday of every week','(306) 162-4684',464.2,1609);
		INSERT INTO service_agreements VALUES('5','85043375','Atlantic Avenue','metal','every Saturday of every week','(923) 798-0938',412.44,2601);

		--Personnel
		INSERT INTO personnel VALUES('34725','Dan','matloff@sbcglobal.net','Windsor Drive','55263');
		INSERT INTO personnel VALUES('42134','Charlotte','mjewell@optonline.net','Maple Avenue','52284');
		INSERT INTO personnel VALUES('16830','Grady','panolex@sbcglobal.net','Hillcrest Avenue','37764');
		INSERT INTO personnel VALUES('73709','Carina','phyruxus@me.com','Schoolhouse Lane','74321');
		INSERT INTO personnel VALUES('15625','Cameron','harryh@icloud.com','Cambridge Court','16391');


		--maintenance_records of drivers owned trucks
		INSERT INTO maintenance_records VALUES('2111','2011-08-30 19:19:46','Inspection');
		INSERT INTO maintenance_records VALUES('2222','2011-08-23 19:19:46','repair');
		INSERT INTO maintenance_records VALUES('2333','2011-08-13 19:19:46','Inspection');
		INSERT INTO maintenance_records VALUES('2444','2011-08-03 19:19:46','repair');

		--maintenance_records of company owned trucks
		INSERT INTO maintenance_records VALUES('1111','2011-08-30 19:19:46','Inspection');
		INSERT INTO maintenance_records VALUES('1222','2011-08-23 19:19:46','repair');
		INSERT INTO maintenance_records VALUES('1333','2011-08-13 19:19:46','Inspection');
		INSERT INTO maintenance_records VALUES('1444','2011-08-03 19:19:46','repair');


		--Dummy containers
		INSERT INTO containers VALUES('NULLID','Dummy Container','2015-03-10 20:42:44');

		--real containers
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



		--information about drivers who own a truck
		INSERT INTO personnel VALUES('12222','Ayub Ahmed','mjewell@optonline.net','Maple Avenue','52284');
			
		--drivers who do not own a truck
		INSERT INTO personnel VALUES('1','Hamda Mare','panolex@sbcglobal.net','Hillcrest Avenue','37764');

		--drivers who own a truck
		INSERT INTO drivers VALUES('12222','Single Trailer','2111');

		--drivers who do not own a truck
		INSERT INTO drivers VALUES('13333','HAZMAT',NULL);
		INSERT INTO service_fulfillments VALUES('2015-07-30 03:47:43','1111111','1','2111','12222','1','NULLID');''')
	connection.commit()



# Creates the tables accessed by the system
def create_tables():
	global connection, cursor

	cursor.executescript('''
	-- CMPUT 291 - Winter 2018 
	-- TABLES for Project #1, assuming SQLite as database engine (uses the TEXT data type) 

	-- The following commands drops the tables in case they exist from earlier runs. 
	DROP TABLE IF EXISTS users;
	DROP TABLE IF EXISTS trucks;
	DROP TABLE IF EXISTS maintenance_records;
	DROP TABLE IF EXISTS containers;
	DROP TABLE IF EXISTS waste_types;
	DROP TABLE IF EXISTS container_waste_types;
	DROP TABLE IF EXISTS personnel;
	DROP TABLE IF EXISTS account_managers;
	DROP TABLE IF EXISTS drivers;
	DROP TABLE IF EXISTS accounts;
	DROP TABLE IF EXISTS service_agreements;
	DROP TABLE IF EXISTS service_fulfillments;


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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ACCOUNT MANAGER Functonality----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def account_managerQ1(username):
global connection, cursor
# We select the customer information of all the customers that the user manages
#then we run our query which outputs the customer information that this manager manages

SELECT 
t1= (username)
cursor.execute('''
		SELECT a.customer_name, a.contact_info,a.customer_type,s.service_no,s.master_account, s.location,s.waste_type,s.pick_up_schedule,s.local_contact,s.internal_cost,s.price 
		FROM accounts a, service_agreements s, account_managers m, personnel p 
		WHERE p.name=? AND p.pid = m.pid AND m.pid = a.account_mgr AND s.master_account = a.account_no ORDER BY s.service_no''', (t1,))
customer_info = cursor.fetchall()
print(customer_info)




#Q2- user adds a new customer account to the database
def account_managerQ2(username):
	global connection, cursor
	#Create a new master account with all the required information. The manager of the account should be automatically set to the id of the account manager who is creating the account.
	#first we select the id of the account manager with the manager name equal to the login name
	t1 = (username,)
	cursor.execute('SELECT  m.pid FROM personnel p, account_managers m WHERE p.pid = m.pid AND p.name = ?', (t1))
	info = cursor.fetchall()
	for i in info:
		for x in i:
			#we now have the manager id
			mid = (x,)
			#grab new customer information from user 
			account_no = raw_input('Enter an account number: ')
			#make sure its len is 8 


			start_date = raw_input('Enter a start_date: ')
			#copy hamses date check
			end_date = raw_input('Enter an end-date: ')
			#copy hamses date check
			
			customer_name = raw_input('Enter a customer_name: ')
			#make sure customer name is not null
			customer_type = raw_input('Enter a customer_type: ')
			#make sure customer type is one of the types that we have

			contact_info = raw_input('Enter customer contact information (ex.000-000-0000): ')
			#make sure format is correct

			total_amount = raw_input('Enter a total amount: ')
			#make sure len is greater than 0


			# now create a new customer account with the manager id
			cursor.execute('INSERT INTO accounts VALUES (?,?,?,?,?,?,?,?);', (str(account_no,),str(mid),str(customer_name,),str(contact_info,),str(customer_type,),str(start_date,),str(end_date,),str(total_amount,)))
			connection.commit()
			time.sleep(0.2)
			print('.....')
			print('Created a new customer account!\n')


			#ask user if they want to add a service agreement to either an existing customer or a customer already int he database
			print('Would you like to create a service agreement for this customer?')
			create_sa = raw_input('Enter Y for Yes or N for No: ')
			#if account manager does not want to add a service agreement to a new customer we ask if they would like to add one for any other customers they manage
			if create_sa == 'N' or 'n':
				print('\n Would you like to create a service agreement for any other customers?')
				sa = raw_input('Enter Y for Yes or N for No: ')
				#if yes we add a service agreement to the another customer 
				if sa == 'Y' or 'y':
					account_managerQ3(username);




			#if user chooses to create a service agreement for the newly added customer
			elif create_sa == 'Y' or 'y':
				#select all the service numbers that we have 
				location = raw_input('Enter a location: ')
				waste_type = raw_input('Enter a waste_type: ')
				pick_up_schedule = raw_input('Enter a pick up schedule: ')
				local_contact = raw_input('Enter a local contact: ')
				internal_cost = raw_input('Enter the internal cost: ')
				price = raw_input('Enter a price: ')
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

				if valid_Q3:
					cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(master_account,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))
					print('\nservice agreement created!')





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
	cursor.execute('SELECT a.customer_name  FROM accounts a WHERE a.account_mgr = ?', (mid,))
	customer_names = cursor.fetchall()
	print(customer_names[0][0])


	#then we get the customer who the account manager wants to make a service agreeement for
	customer_name = raw_input('\nWhat is the name of the customer you want to create a service agreement for?: ')
	if customer_names[0][0] == customer_name:

		print(customer_names[0][0])

		cursor.execute('SELECT a.account_no,a.account_mgr FROM accounts a, account_managers m WHERE a.customer_name = ?',((customer_name,)))
		account_num = cursor.fetchall()
		a_mgr = account_num[0][1]
		a_no = account_num[0][0]


		#if account manager selects a cusotmer that they do not manage we exit
		#then we print the customer names fro the user to select from 
		if a_mgr != mid:
			print('Sorry you do not manage this customer')
		
		#account manager selects a customer they manage and we grab service agreement information
		else:
		#randomly select a service number 
			service_no = random.randint(0,100)
			cursor.execute('SELECT service_no FROM service_agreements')
			badSA = cursor.fetchall()
			#if randomly selected service number is in use randomly select another one 
			for i in badSA:
				if i[:] == service_no:
					print(i)
					service_no.random.randint(0,100)
					print(service_no)
				
				else:
				#prompt user to enter values for a service agreement 
					location = raw_input('Enter a location: ')
					waste_type = raw_input('Enter a waste_type: ')
					pick_up_schedule = raw_input('Enter a pick up schedule: ')
					local_contact = raw_input('Enter a local contact: ')
					internal_cost = raw_input('Enter the internal cost: ')
					price = raw_input('Enter a price: ')

					#if the information is valid then we create a service agreement account for this customer
					valid_Q3(location, waste_type, pick_up_schedule,local_contact, internal_cost,price)
					
					#if user inputted information is correctly inputted then we create a new service agreement for the customer
					if valid_Q3 and i != service_no:
						cursor.execute('INSERT INTO service_agreements VALUES(?,?,?,?,?,?,?,?)',(str(service_no,),str(a_no,),str(location,),str(waste_type,),str(pick_up_schedule,),str(local_contact,),str(internal_cost,),str(price,)))
						print('\nService agreement created!')
						break




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
	cursor.execute('SELECT a.customer_name  FROM accounts a WHERE a.account_mgr = ?', (mid,))
	customer_names = cursor.fetchall()
	for i in customer_names:
		print i[0]


	#as user to enter customer name
	customer_name = raw_input('\nWhat is the name of the customer who you want to see a summary report for?: ')

	#if customer name matches with the customer names that the user manages
	print(customer_names[0][0])
	if str(customer_names[0][0]) == customer_name:
		#select the count of services, sum of internal cost, sum of prices, and the count of the different waste types
		cursor.execute('SELECT COUNT(s.service_no), SUM(s.internal_cost),SUM(s.price), FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = a.account_no AND a.customer_name = ?' ,((customer_name,)))
		connection.commit()
		summary = cursor.fetchall()
		#print the summary for the user
		cursor.execute('SELECT COUNT(*)  FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = a.account_no AND a.customer_name = ? GROUP BY s.waste_type' ,((customer_name,)))
		cursor.commit()
		waste_types = cursor.fetchall()
		distinct_types = len(waste_types)

		for i in summary:
			i = newsummary
		print(distinct_types)

	#if user inputs a customer name that does not match with the customers they manage, add this to the top as a while loop
	#condition, user must manage this account 
	else:
		print('Sorry you do not manage this customer')
		




# linkes account managers to the many options account managers have
#add the enter q to logout statement
def account_manager(username):
	global connection, cursor
	print()
	print("-------------------------------------------------------------")
	print("ACCOUNT MANAGER PAGE:")
	print("-------------------------------------------------------------")
	print() 'Welcome Account Manager'
	print
	logout = input('Enter q to exit')
	if logout == q:
		logout()

	else:
		print('What would you like to do?')
		options = raw_input(' Enter 1 to view the customer information of all customers that you manage:\n Enter 2 to create a new customer account:\n Enter 3 to create a new service agreement for an existing customer:\n Enter 4 to view a customers summary: ')

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
#-------------------------------------------SUPERVISOR FUNCTIONALIT----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def supervisor():
	pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------DRIVER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def driver():
	global connection, cursor

	#Get the start date
	while True:
		start_date= input("ENTER START DATE (FORMAT YYYY-MM-DD): ")
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
#-------------------------------------------DISPATCHER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def dispatcher():
	global connection, cursor

	print("WELCOME DISPATCHER!!")
	print("\n\n")

	# Select a service_agreement, driver, truck, and a container to be dropped off and picked up
	
	# Select a service no for a particular service agreement
	service_no= Dispatcher_getService_no()

	# find master account
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

	#Create entries in the table service_fulfillments for upcoming days
	add_service_fulliment(date, master_account, service_no, truck, driver, cid_drop_off, cid_pick_up)




# Add the entry to the service_fulliment table with the following data
def add_service_fulliment(date_time, master_account, service_no, truck_id, driver_id, cid_drop_off, cid_pick_up):
	global connection, cursor

	cursor.execute('''
		INSERT INTO service_fulfillments VALUES(?,?,?,?,?,?,?)''',(date_time, master_account, service_no, truck_id, driver_id, cid_drop_off, cid_pick_up) )
	connection.commit()


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
		if(driver not in drivers_list):
			continue
		else:
			break
	return driver

# QUESTION 1
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
			if(truck not in truck_list):
				continue
			else:
				break

	else:
		# GET THE TRUCK
		truck= num
	
	return truck

# QUESTION 2
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

# QUESTION 3
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
		if(container not in container_list):
			continue
		else:
			break

	# Return the container being dropped off
	return container

# Question 4
# Set the date for a particular entry
def setDate():

	date_array=[]
	print("ENTER DATE (FORMAT YYYY-MM-DD): ")


	date_list=[]

	while True:

		while True:


			date= input("ENTER DATE (FORMAT YYYY-MM-DD): ")
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
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
			
			


#Checks the database to authenticate what the user entered is correct
def Authenticate(entered_pwd,username):
	global connection, cursor

	status = False
	# Hashed it using code given
	hash_name = 'sha256'
	salt = 'ssdirf993lksiqb4'
	iterations = 100000

	t1=(username,)
	#Selects the password from the table associated to the user
	cursor.execute('SELECT password FROM users WHERE login==?',t1)
	connection.commit()
	rows = cursor.fetchall()

	#If hashed password is the same as the hashed database password then login is successful
	print(entered_pwd)
	print(rows)
	if(rows!=[]):
		for row in rows:
			print(row)
			print(row[0])
			dk=row[0]
			dk2 = encrypt_password(entered_pwd)
			if dk == dk2:
				status = True	
	return status



#assume user is not in the users table
def encrypt_password(password):
	global connection, cursor
	status = False
	# Hashed it using code given
	hash_name = 'sha256'
	salt = 'ssdirf993lksiqb4'
	iterations = 100000
	dk =pbkdf2_hmac(hash_name, bytearray(password, 'ascii'), bytearray(salt, 'ascii'), iterations)

	return dk



def create_account():
	global cursor, connection

	print()
	print()
	print("-------------------------------------------------------------")
	print("CREATE ACCOUNT PAGE:")
	print("-------------------------------------------------------------")
	print('Enter q to exit')
	#PID
	#Make sure that pid is in personnel
	while True:
		pid = input('Please enter your personnel identification number: ')	
		if (pid=="q" or pid=="Q"):
			logout()
		cursor.execute('''
			select *
			from personnel
			where pid=?''', (pid,))
		row=cursor.fetchall
		if row==[]:
			continue
		else:
			break

	#USERNAME
	#Make sure the username is unique
	while True:
		username = input('Please enter a username to Login: ')
		if (pid=="q" or pid=="Q"):
			logout()
		cursor.execute('''
			select *
			from users
			where login=?''', (username,))
		row=cursor.fetchall()

		if row!=[]:
			continue
		else:
			break

	

	#PASSWORD
	password = input('Please enter a password to Login: ')
	encrypt_pass = encrypt_password(password)

	#ROLE
	role=get_role(pid)

	t=(pid,role,username,encrypt_pass)
	
	#insert user information into the users table
	cursor.execute('INSERT INTO users VALUES(?,?,?,?)',t)
	connection.commit()
	# Call to login
	print()
	print()
	login()


def get_role(pid):
	global cursor, connection
	#case1: Account Manager Table
	cursor.execute('''
		SELECT *
		FROM personnel p, account_managers a
		WHERE p.pid=a.pid
		AND p.pid=?''', (pid,))
	connection.commit()
	acccount_manager_table=cursor.fetchall()


	#case2: Driver Table
	cursor.execute('''
		SELECT *
		FROM personnel p, drivers d
		WHERE p.pid=d.pid
		AND p.pid=?''', (pid,))
	connection.commit()
	driver_table=cursor.fetchall()

	#case3: Supervisor
	cursor.execute('''
		SELECT *
		FROM personnel p
		WHERE p.supervisor_pid=?''', (pid,))
	connection.commit()
	supervisor_table=cursor.fetchall()

	print(acccount_manager_table) 
	print(driver_table)
	print(supervisor_table)

	#case1
	if acccount_manager_table!=[]:
		role="account manager"
	#case2
	elif driver_table!=[]:
		role="driver"
	#case3
	elif supervisor_table!=[]:
		role="supervisor"
	#case4
	else:
		role="dispatcher"

	return role



#Allows user to log in succesfully with previous username and previous password
def login():
	print()
	print()
	print("-------------------------------------------------------------")
	print("LOGIN PAGE:")
	print("-------------------------------------------------------------")
	count=0

	while count<3:
		print("ATTEMPTS REMAINING: %d" % (3-count) )
		#if user has logged out we dont have to login
		if logout == True:
			break

		#get username

		username = input("Please enter your username: ")
		# Check to see if user enetered q to quit
		if (username=="q" or username=="Q"):
			print ('GoodBye')
			break
		
		#get password
		psw = input("Please enter your password: ")
		print ('\n')
		print ('Authenticating............')
		time.sleep(0.3)
		
		# Check to see if user enetered q to quit
		if (psw=="q" or psw=="Q"):
			print('GoodBye')
			break

		#If hashed password is the same as the hashed database password then login is successful
		status = Authenticate(psw,username)
		# If Login is not successful, loop back to login
		if not status:
			print("\nUsername and Password do not match")
			count=count+1
		#if the user successfully logged in we find its roles
		if status:
			start(username)


def logout():
	print()
	print("Goodbye!")
	exit(0)



def start(username):
	print()
	while True:
		print('Enter q to exit when Prompted to enter data!!!')
		role = find_role(username)
		print(role)
		Role_GateKeeper(role, username)



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


	decision= input('PRESS L TO LOGIN IN, OR PRESS C TO CREATE AN ACCOUNT: ')
	
	if decision == 'C' or decision== 'c':
			create_account()
	
	elif decision == 'L' or  decision=='l':
		login()

	print()
	print()
	print("GoodBye")
	
main()
	


