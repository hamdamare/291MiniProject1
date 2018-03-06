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




#Checks the database to authenticate what the user entered is correct
def Authenticate(username, entered_pwd):
	global connection, cursor

	# Hashed it using code given
	hash_name = 'sha256'
	salt = 'ssdirf993lksiqb4'
	iterations = 100000
	dk = pbkdf2_hmac(hash_name, bytearray(entered_pwd, 'ascii'), bytearray(salt, 'ascii'), iterations)
	

	#Get user password from database 
	t1= (username,)
	cursor.execute('''
		select password 
		from users
		where login=?''', t1)
	database_pwd= cursor.fetchone()
	connection.commit()


	# Check if password exists
	if (dk==database_pwd):
		return True

	else:
		return False

			
def account_manager():
	pass

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

	logout=True





# Function find_role returns the role associated to that particular username
def find_role(username):
	t1= (username,)
	cursor.execute('''
		select role 
		from users
		where login=?''', t1)
	role= cursor.fetchone()
	# Return the role of the user
	return role







def main():
	global connection, cursor, logout

	# Initialized the path to the database
	connection= sqlite3.connect("./waste_management.db")
	# Set the cusor to the cursor of the database
	cursor= connection.cursor()

	# Call to the Create Table Function
	create_tables()

	# Loop to login to the system 
	while (logout==False):

		# Get username from user
		username = input('Enter username or Enter q to exit: ')
		# Check to see if user enetered q to quit
		if (username=="q" or username=="Q"):
			break

		else: 
			# get password from password
			pwd = input('Enter a password or Enter q to exit: ')
			# Check to see if user enetered q to quit
			if (pwd=="q" or pwd=="Q"):
				break

			# Call to authenticate the user
			status=Authenticate(username, pwd)

			# If login successful find a role
			if status==True:
				role= find_role(username)
				role_GateKeeper(role)

			# Else Login is not successful, loop back to login 
			else:
				print("Username and password do not Match")
				print()
				print()
				continue	

	print()
	print()	
	print("GoodBye")





main()
	


