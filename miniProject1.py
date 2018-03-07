# Citations

# Import modules
from hashlib import pbkdf2_hmac
import time
import sqlite3

# Global variables
connection = None
cursor = None
logout=False


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
	connection.commit()

def insert_data():
	cursor.executescript('''
		--information about account managers
	INSERT INTO personnel VALUES('34725','Dan','matloff@sbcglobal.net','Windsor Drive','55263');
	INSERT INTO personnel VALUES('42134','Charlotte','mjewell@optonline.net','Maple Avenue','52284');
	INSERT INTO personnel VALUES('16830','Grady','panolex@sbcglobal.net','Hillcrest Avenue','37764');
	INSERT INTO personnel VALUES('73709','Carina','phyruxus@me.com','Schoolhouse Lane','74321');
	INSERT INTO personnel VALUES('15625','Cameron','harryh@icloud.com','Cambridge Court','16391');


	INSERT INTO users VALUES('34725','Account manager','Dan','pass1');
	INSERT INTO users VALUES('42134','Account manager','Charlotte','pass2');
	INSERT INTO users VALUES('16830','Account manager','Grady','pass3');
	INSERT INTO users VALUES('73709','Account manager','Carina','pass4');
	INSERT INTO users VALUES('15625','Account manager','Cameron','pass5');

	INSERT INTO account_managers VALUES('34725','small accounts manager','8th Street South');
	INSERT INTO account_managers VALUES('42134','major accounts manager','Main Street West');
	INSERT INTO account_managers VALUES('16830','medium accounts manager','Magnolia Court');
	INSERT INTO account_managers VALUES('73709','medium accounts manager','Route 4');
	INSERT INTO account_managers VALUES('15625','medium accounts manager','Park Avenue');

	INSERT INTO accounts VALUES('87625036','34725','Rhianna Wilkinson','(201) 874-4399','residential','2006-05-19 13:16:14','2018-02-12 06:50:29',837646.52);
	INSERT INTO accounts VALUES('73833854','42134','Reese Thornton','(745) 516-3060','commercial','2004-01-18 03:26:06','2013-02-09 15:56:27',893618.73);
	INSERT INTO accounts VALUES('34910788','16830','Jarrett Castro','(883) 338-6912','commercial','2007-01-28 20:29:51','2019-11-06 10:14:50',658737.09);
	INSERT INTO accounts VALUES('12029871','73709','Areli Lowery','(706) 692-2734','industrial','2000-08-03 20:48:36','2018-03-07 04:15:21',322370.9);
	INSERT INTO accounts VALUES('85043375','15625','Lilyana Gaines','(425) 810-3987','municipal','2003-04-02 7:38:38','2016-02-10 21:45:17',111695.11);


	INSERT INTO service_agreements VALUES('1','87625036','Elm Avenue','hazardous waste','every Tuesday of every week','(904) 694-9532',566.45,1994);
	INSERT INTO service_agreements VALUES('2','73833854','Essex Court','mixed waste','every Wednesday of every week','(947) 900-1946',657.8,1643);
	INSERT INTO service_agreements VALUES('3','34910788','Circle Drive','construction waste','every Monday of every week','(149) 953-8810',360.87,1225);
	INSERT INTO service_agreements VALUES('4','12029871','Delaware Avenue','hazardous waste','every Friday of every week','(306) 162-4684',464.2,1609);
	INSERT INTO service_agreements VALUES('5','85043375','Atlantic Avenue','metal','every Saturday of every week','(923) 798-0938',412.44,2601);
	''')
	connection.commit()


		
def account_manager(username):
	global connection, cursor
	# We select the customer information of all the customers that the user manages
	#then we run our query which outputs the customer information that this manager manages
	cursor.execute('''SELECT DISTINCT s.service_no,a.customer_name, a.contact_info, a.customer_type
	FROM accounts a, service_agreements s, account_managers m, personnel p
	WHERE s.master_account = a.account_no AND a.account_mgr = m.pid AND p.pid= username
	GROUP BY s.service_no
	;''')
	connection.commit()
def supervisors():
	pass

def dispatchers():
	pass

def drivers():
	pass

# Depending on the role, GateKeeper for that tasks asociated to that role
def Role_GateKeeper(role):

	if (role=="Account managers"):
		account_manager()

	elif (role== "Supervisors"):
		supervisors()

	elif (role== "Dispatchers"):
		dispatchers()

	else:
		drivers()




# Logs user out of the system
def LogOut():
	global connection, cursor, logout

	logout=False
	return logout



# Function find_role returns the role associated to that particular username
def find_role(username):
	t1= (username,)
	cursor.execute('''
		select role 
		from users
		where login=?''', t1)
	role = cursor.fetchone()
	# Return the role of the user
	return role


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
	cursor.execute('SELECT password FROM users WHERE login = ?',t1)
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
	logout = LogOut()

	while not logout:
		print'_____________________WELCOME_____________________'
		print 5*'\n'

		#get username
		username = raw_input("Please enter your username: ")
		print '\n'
		# Check to see if user enetered q to quit
		if (username=="q" or username=="Q"):
			print 'GoodBye'
			break
		
		#get password
		psw = raw_input("Please enter your password: ")
		print '\n'
		# Check to see if user enetered q to quit
		if (username=="q" or username=="Q"):
			print 'GoodBye'
			break


		t1=(username,)
		#Selects the password from the table associated to the user
		cursor.execute('SELECT password FROM users WHERE login = ?',t1)
		rows = cursor.fetchall()

		#If hashed password is the same as the hashed database password then login is successful
		status = Authenticate(psw,username)


		# If Login is not successful, loop back to login
		if status != True:
			print("Username and password do not Match")
			print 2*'\n'
			continue


		if status == True:
			print"Welcome ",  username
			role = find_role(username)
			Role_GateKeeper(role)
			break
		

def main():
	global connection, cursor, logout

	# Initialized the path to the database
	connection= sqlite3.connect("./waste_management.db")
	# Set the cusor to the cursor of the database
	cursor= connection.cursor()
	# Call to the Create Table Function
	create_tables()
	# Call to populate the tables
	insert_data()

	# Loop to login to the system 
	login()
	if LogOut == True:
		print
		print	
		print("GoodBye")





main()
	


