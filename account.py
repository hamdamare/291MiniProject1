		
# Import modules
from hashlib import pbkdf2_hmac
from datetime import datetime
import time
import sqlite3
import datetime
import time
import re
import random 

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

		INSERT INTO personnel VALUES('34725','Dan','matloff@sbcglobal.net','Windsor Drive','55263');
		INSERT INTO personnel VALUES('42134','Charlotte','mjewell@optonline.net','Maple Avenue','52284');
		INSERT INTO personnel VALUES('16830','Grady','panolex@sbcglobal.net','Hillcrest Avenue','37764');
		INSERT INTO personnel VALUES('73709','Carina','phyruxus@me.com','Schoolhouse Lane','74321');


		INSERT INTO users VALUES('34725','Account manager','Dan','pass1');
		INSERT INTO users VALUES('42134','Account manager','Charlotte','pass2');




		INSERT INTO account_managers VALUES('34725','small accounts manager','8th Street South');
		INSERT INTO account_managers VALUES('42134','major accounts manager','Main Street West');






		INSERT INTO accounts VALUES('87625036','34725','Rhianna Wilkinson','(201) 874-4399','residential','2006-05-19 13:16:14','2018-02-12 06:50:29',837646.52);
		INSERT INTO accounts VALUES('73833854','42134','Reese Thornton','(745) 516-3060','commercial','2004-01-18 03:26:06','2013-02-09 15:56:27',893618.73);




		INSERT INTO service_agreements VALUES('1','87625036','Elm Avenue','hazardous waste','every Tuesday of every week','(904) 694-9532',566.45,1994);
		INSERT INTO service_agreements VALUES('2','73833854','Essex Court','mixed waste','every Wednesday of every week','(947) 900-1946',657.8,1643);

	
		--drivers who own a truck
		INSERT INTO drivers VALUES('12222','Single Trailer','2111');

		--drivers who do not own a truck
		INSERT INTO drivers VALUES('13333','HAZMAT',NULL);
		INSERT INTO service_fulfillments VALUES('2015-07-30 03:47:43','1111111','1','2111','12222','1','NULLID');
		''')


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
	  FOREIGN KEY (waste_type) REFERENCES waste_types); 
	  
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
	  FOREIGN KEY (cid_pick_up) REFERENCES containers(container_id));
	''')



	cursor.execute(' PRAGMA forteign_keys=ON; ')
	connection.commit()





#checks validity of user eneterd information for a new customer 
def valid_Q3(account_no,start_date,end_date,customer_name,customer_type,contact_info,total_amount):
	valid_q3 = False
	'''count = 1;
	while not valid_q3:
		#check if  user enters proper account number
		if re.match('^[0-9]{8}$',account_no) == False:
		print('Sorry you did not enter a valid account number')
		account_no = raw_input('Enter an account number(8 digits): ')
		else:
			count += 1

		if count == 2:
		`	#check if user enterd the right date in the right format
			if re.match('^[0-9]{3}-[0-9]{2}-[0-9]{2}$',start_date) = False:
				print('Sorry you did not enter a valid date (YYYY-MM-DD OR YYYY-DD-MM)')
				start_date = raw_input('Enter a start_date (ex.YYYY-MM-DD OR YYYY-DD-MM): ')
			else:
				count += 1

		if count == 3:
			#check if user enterd the right date in the rigth format
			if re.match('^[0-9]{3}-[0-9]{2}-[0-9]{2}$',start_date) = False:
				print('Sorry you did not enter a valid date (YYYY-MM-DD OR YYYY-DD-MM)')
				end_date = raw_input('Enter an end-date (YYYY-MM-DD OR YYYY-DD-MM): ')
			else:
				count += 1

		if count == 4:
			#check if customer_name is correct
			if !customer_name.isalpha():
				print('Sorry you did not enter a valid customer name(ex 'Dan')')
				customer_name = raw_input('Enter a customer_name(ex.'Dan'): ')
			else:
				count+= 1

		if count == 5:
			#check if valid customer type
			if customer_type != 'industrial' or 'residential' or 'commercial' or 'municipal':
				print('Sorry you ddi not enter a valid customer type(residential,industrial,commercial,or municipal) ')
				customer_type = raw_input('Enter a customer_type(residential,industrial,commercial,or municipal): ')
			else:
				count+=1

		if count == 6:
			#check if user entered the right phone numebr in the right order
			if re.match('^[0-9]{3}-[0-9]{3}-[0-9]{4}$', contact_info) = False:
				print('sorry you did not enter a valid phone number(ex.000-000-0000)')
				contact_info = raw_input('Enter customer contact information (ex.000-000-0000): ')
			else:
				count += 1

		#check if valid totoal amount

		if count == 7:
			if type(total_amount)!= type(int):
				print('Sorry you did not enter a valid amount(ex.50)')
				total_amount = raw_input('Enter a total amount: ')

			else:
				count += 1

		'''
			return  valid_q3 = True;



			
			
			
			
			
	#call validate after every user input then we have determine if what the user currently inputterd is right
	#neeed a while loop for when user is inputing location 



def valid_Q4(location, waste_type, pick_up_schedule,local_contact, internal_cost,price):
	valid_q4 = False
	'''count = 1;


	while not valid_q4:
	#check if  we have a location 
	if len(location) > 1:
			count+=1

	else:
		print('Sorry you did not enter a location')

		
		if re.match('^[0-9]{8}$',account_no) == False:
		print('Sorry you did not enter a valid account number')
		account_no = raw_input('Enter an account number(8 digits): ')
		else:
			count += 1

		if count == 2:
		`	#check if user enterd the right date in the right format
			if re.match('^[0-9]{3}-[0-9]{2}-[0-9]{2}$',start_date) = False:
				print('Sorry you did not enter a valid date (YYYY-MM-DD OR YYYY-DD-MM)')
				start_date = raw_input('Enter a start_date (ex.YYYY-MM-DD OR YYYY-DD-MM): ')
			else:
				count += 1

		if count == 3:
			#check if user enterd the right date in the rigth format
			if re.match('^[0-9]{3}-[0-9]{2}-[0-9]{2}$',start_date) = False:
				print('Sorry you did not enter a valid date (YYYY-MM-DD OR YYYY-DD-MM)')
				end_date = raw_input('Enter an end-date (YYYY-MM-DD OR YYYY-DD-MM): ')
			else:
				count += 1

		if count == 4:
			#check if customer_name is correct
			if !customer_name.isalpha():
				print('Sorry you did not enter a valid customer name(ex 'Dan')')
				customer_name = raw_input('Enter a customer_name(ex.'Dan'): ')
			else:
				count+= 1



		#check if valid internal cost
		if count == 4:
			if type(price)!= type(int):
				print('Sorry you did not enter a valid amount(ex.50)')
				total_amount = raw_input('Enter a total amount: ')

			else:
				count += 1
		if count == 5:
			type(internal_cost) != type(int):
			print('Sorry you did not enter a valid amount(ex.50)')

		else:
			count+=1
				
		if count == 8:
			return  valid_q4 = True;
'''

	return True


#Q1- select customer and list all info associated with this customer, followed by a list of their individual service agreements 
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
			start_date = raw_input('Enter a start_date: ')
			end_date = raw_input('Enter an end-date: ')
			
			customer_name = raw_input('Enter a customer_name: ')
			customer_type = raw_input('Enter a customer_type: ')

			contact_info = raw_input('Enter customer contact information (ex.000-000-0000): ')
			total_amount = raw_input('Enter a total amount: ')



			if valid_info(account_no,start_date,end_date,customer_name,customer_type,contact_info,total_amount):
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
					valid_Q3(location, waste_type, pick_up_schedule,local_contact, internal_cost,price)
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
		cursor.execute('SELECT DISTINCT COUNT(s.service_no), SUM(s.internal_cost),SUM(s.price),COUNT(s.waste_type) FROM accounts a, account_managers m, service_agreements s WHERE a.account_mgr = m.pid AND s.master_account = a.account_no AND a.customer_name = ?',((customer_name,)))
		summary = cursor.fetchall()
		#print the summary for the user
		for i in summary:
			print(i)
	#if user inputs a customer name that does not match with the customers they manage
	else:
		print('Sorry you do not manage this customer')
		


# linkes account managers to the many options account managers have
def account_manager(username):
	global connection, cursor
	print 'Welcome Account Manager',username
	print
	print 

	print('What would you like to do?')
	options = raw_input(' Enter 1 to view the customer information of all customers that you manage:\n Enter 2 to create a new customer account:\n Enter 3 to create a new service agreement for an existing customer:\n Enter 4 to view a customers summary: ')
	if options =='1':
		account_managerQ1(username)

	elif options == '2':
		account_managerQ2(username)

	elif options == '3':
		account_managerQ3(username)

	elif options == '4':
		account_managerQ4(username)




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
	rows = cursor.fetchall()
	#If hashed password is the same as the hashed database password then login is successful
	for row in rows:
		db_pass = row[0]
		dk = pbkdf2_hmac(hash_name, bytearray(entered_pwd, 'ascii'), bytearray(salt, 'ascii'), iterations)
		dk2 =pbkdf2_hmac(hash_name, bytearray(db_pass, 'ascii'), bytearray(salt, 'ascii'), iterations)
		if dk == dk2:
			status = True	
	return status



#Allows user to log in succesfully with previous username and previous password
def login():
	global cursor, connection
	#logout is whether or not user has logged out
	login = False
	#user must not have logged in yet to login
	while not login:
		#if user has logged out we dont have to login
		#if logout == True:
			#break

		#get username
		username = raw_input("Please enter your username: ")
		

		# Check to see if user enetered q to quit
		if (username=="q" or username=="Q"):
			print ('GoodBye')
			break


		# Check to see if user enetered q to quit
		if (psw=="q" or psw=="Q"):
			print('GoodBye')
			break
		
		#get password
		psw = raw_input("Please enter your password: ")
		print ('\n')
		encrypt_password(username)
		print ('Authenticating............')
		time.sleep(0.3)
		



		#If hashed password is the same as the hashed database password then login is successful
		status = Authenticate(psw,username)
		# If Login is not successful, loop back to login
		if not status:
			print("\nUsername and Password do not match")
			continue
		#if the user successfully logged in we find its roles
		if status:
			print
			find_role(username)
			break





def new_user(username,password):
	global cursor, connection
	new_pass = (hashed password)
	t1 = username;
	cursor.execute('SELECT role FROM personnel WHERE login = ?', (t1,))
	data = cursor.fetchall()
	for i in data:
		if i[0] == driver:
			insert data into the users table 

		elif i[0] == account_manager:
			insert data into the users table

		elif i[0]  == supervisors:
			insert data into users

		elif i[0] == dispatcher:
			insert data into users


			



def find_role(username):
	global connection, cursor

	t1 = (username,)
	#find roles of users
	cursor.execute('SELECT role FROM users WHERE login=?', t1)
	role = cursor.fetchall()
	connection.commit()
	# Return the role of the user
	for i in role[0]:
		if i == 'Account manager':
			account_manager(username)


def main():
	global connection, cursor, logout

	# Initialized the path to the database
	connection= sqlite3.connect("./waste_management.db")
	# Set the cusor to the cursor of the database
	cursor= connection.cursor()
	# Call to the Create Table Function
	create_tables()
	# Loop to login to the system 
	add_data()
	login()
	#if LogOut == True:
		#print()
		#print()
		#print("GoodBye")
		

main()