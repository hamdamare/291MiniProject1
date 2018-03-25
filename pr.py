import sqlite3
connection = None;
cursor = None;


 #Mainn function
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
        print('logout')

    elif decision == 'C' or decision== 'c':
        print('create account')
    
    elif decision == 'L' or  decision=='l':
        print('login')

    print()
    
main()
    
