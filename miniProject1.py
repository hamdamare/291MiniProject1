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

		--Users 
		INSERT INTO users VALUES('34725','Account manager','Dan','pass1');
		INSERT INTO users VALUES('42134','Account manager','Charlotte','pass2');
		INSERT INTO users VALUES('16830','Account manager','Grady','pass3');
		INSERT INTO users VALUES('73709','Account manager','Carina','pass4');
		INSERT INTO users VALUES('15625','Account manager','Cameron','pass5');
		INSERT INTO users VALUES('56468','Account manager','Roderick','pass6');
		INSERT INTO users VALUES('81480','Account manager','Katrina','pass7');
		INSERT INTO users VALUES('48660','Account manager','Jeremy','pass8');

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
		INSERT INTO personnel VALUES('13333','Hamda Mare','panolex@sbcglobal.net','Hillcrest Avenue','37764');

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


def supervisors():
	pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ACCOUNT MANAGER Functonality----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def account_manager():
	pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------SUPERVISOR FUNCTIONALIT----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def supervisor():
	pass

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------DRIVER FUNCTIONALITY----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def driver():
	pass


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
	add_service_fulliment(date, '2', service_no, truck, driver, cid_drop_off, cid_pick_up)




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
		container= 'NULLID'
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
	while True:
		# GET THE YEAR
		while True:
			year=input("ENTER THE YEAR (FORMAT YYYY) : ")
			if len(year)==4:
				date_array.insert(0,year)
				break
			else:
				continue

		# GET THE MONTH
		month_list=['1','2','3','4','5','6','7','8','9','10','11','12']
		while True:
			month=input("ENTER MONTH (FORMAT MM) : ")
			if month in month_list:
				date_array.insert(1,month)
				break
			else:
				continue
		
		# GET THE DAY
		while True:
			day= int(input("ENTER DATE (FORMAT DD) : "))
			if day<=31 and day>0:
				date_array.insert(2,str(day))
				break
			else:
				continue
		# Validate the date the user entered
		date= datetime.datetime.strptime(date_array[0]+'-'+date_array[1]+'-'+date_array[2], '%Y-%m-%d')
		print(date)
		print(datetime.datetime.now())
		if(datetime.datetime.now()<date):
			break
		else:
			#print("TRY AGAIN (DATE HAS PASSED, ", end=" ")
			continue
	# return the date
	return date
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Logs user out of the system
def LogOut():
	global connection, cursor, logout
	logout=False
	return logout

# Function find_role returns the role associated to that particular username
def find_role(username):
	global connection, cursor

	t1= (username,)
	cursor.execute('SELECT role FROM users WHERE login=?', t1)
	role = cursor.fetchall()
	connection.commit()
	# Return the role of the user
	return role[0]
	print(role)


# Depending on the role, GateKeeper for that tasks asociated to that role
def Role_GateKeeper(role):
	global logout
	while logout==False:
		if (role=="account manager"):
			account_manager()
			break
			
		elif (role== "supervisor"):
			supervisor()
			break
			
		elif (role== "dispatcher"):
			dispatcher()
			break
			
		else:
			driver()
			break
			


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
		if logout == True:
			break
		print'\n'

		#get username
		username = raw_input("Please enter your username: ")
		# Check to see if user enetered q to quit
		if (username=="q" or username=="Q"):
			print 'GoodBye'
			break
		
		#get password
		psw = raw_input("Please enter your password: ")
		print '\n'
		print 'Authenticating............'
		time.sleep(0.3)
		

		# Check to see if user enetered q to quit
		if (psw=="q" or psw=="Q"):
			print 'GoodBye'
			break

		#If hashed password is the same as the hashed database password then login is successful
		status = Authenticate(psw,username)
		# If Login is not successful, loop back to login
		if not status:
			print("\nUsername and password Do Not Match")
			print
			continue
		#if the user successfully logged in we find its roles
		if status:
			print "\nWelcome",username
			login = True
			role = find_role(username)
			Role_GateKeeper(role)


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
	if LogOut == True:
		print
		print	
		print("GoodBye")
	

main()
	


