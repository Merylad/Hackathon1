import psycopg2
import getpass

class UsersDB:
    def __init__(self):
        self.connection = psycopg2.connect(
        database = 'hangman',
        user = 'postgres',
        password = 'root',
        host = '127.0.0.1',
        port = 5432
        )

        self.cursor = self.connection.cursor()
        
    def register_or_connect(self):
        self.username = input('Enter your username: ')
        

        query = f"SELECT username FROM users WHERE username = '{self.username}';"
        self.cursor.execute(query)
        existing_user = self.cursor.fetchone()

        if existing_user:
            print("User exists. Connecting...")
            self.connect_user()
        else:
            print("User does not exist. Registering...")
            self.register()
     
        
    def register (self):
        password = getpass.getpass("Enter your password: ")              
        query = f'''
        INSERT INTO users( username, password)
        VALUES ('{self.username}','{password}');
        '''
        
        self.cursor.execute(query)
        self.connection.commit()
        
        query = f'''
        INSERT INTO game_results (win, lost, user_id)
        VALUES (0,0,(SELECT user_id FROM users WHERE username = '{self.username}'))
        '''
        self.cursor.execute(query)
        self.connection.commit()
        print("User registered successfully.")
        
        
 
            
    def connect_user (self):
        while True:
            password = getpass.getpass("Enter your password: ")
            query = f'''
            SELECT password FROM users WHERE username = '{self.username}';
            '''
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            
            if password == result[0]:
                print ("User connected successfully.")
                break
            else:
                print("Invalid password. Connection failed.")
                
    def add_results (self, results):

        # Check if the user exists in the game_results table
        check_query = f'''
        SELECT user_id FROM game_results WHERE user_id IN ( SELECT user_id FROM users WHERE username = '{self.username}')
        '''
        self.cursor.execute(check_query)
        existing_user = self.cursor.fetchone()
    
        if results:
            query = f'''
            UPDATE game_results
            SET win = win + 1
            WHERE user_id IN ( SELECT user_id FROM users WHERE username = '{self.username}')
            '''
        else:
            query = f'''
            UPDATE game_results
            SET lost = lost + 1
            WHERE user_id IN ( SELECT user_id FROM users WHERE username = '{self.username}')
            '''
    
        self.cursor.execute(query)
        self.connection.commit()
        
    def display_results(self):
        query = f'''
        SELECT win, lost FROM game_results WHERE user_id IN (SELECT user_id FROM users WHERE username='{self.username}')
        '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print (f"{self.username}'s results: \n" + 
               f"win : {result[0]} \n"  +
               f"lost: {result[1]} \n")
        
    
                
            
        
    def close_connection(self):
        self.cursor.close()
        self.connection.close()
        
    
# meryl = UsersDB()
# meryl.register_or_connect()
# meryl.close_connection()