import mysql.connector
from dotenv import load_dotenv
import os
from backend.utils import hash_salt

'''
Using the current environment
(mainly SQL_USER, SQL_DATABASE, and SQL_PASSWORD)
provides functions to interact with SQL database.
'''

load_dotenv()

# if account with id exists, will return float
# otherwise returns None
# (assumes correct data types)
def check_balance(id):
  # load DB
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = (f"""
           SELECT balance FROM account
           WHERE id={id};
           """
  )

  cursor.execute(query)

  bal = None

  # have to type cast or else errors with SQL
  for item in cursor:
    bal = float(item[0])

  cursor.close()
  connection.close()

  return bal

# if account with id exists, adds specified amount
# of money and returns NEW balance. 
# if doesn't exist, returns None
# (assumes correct data types)
def deposit(id, amount):
  # make sure account exists
  # AND get current balance
  current_bal = check_balance(id)
  
  if current_bal is None:
    return None

  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = (f"""
            UPDATE account
            SET balance = balance + {amount}
            WHERE id = {id};
            """
  )

  cursor.execute(query)
  cursor.close()

  # REALLY IMPORTANT TO COMMIT
  connection.commit()
  connection.close()

  # essentially "fake" re-getting the new balance
  return current_bal + amount

# if account with id exists, checks if enough money
#  if not enough, returns what the negative balance would've been
#  if is enough, removes that much money and returns NEW balance
# if account doesn't exist, returns None
# (assumes correct data types)
def withdraw(id, amount):
  # makes sure account exists
  # AND gets current balance
  current_bal = check_balance(id)
  
  if current_bal is None:
    return None
  
  # make sure can actually withdraw that amount
  if (neg_diff := current_bal - amount) < 0:
    return neg_diff

  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = (f"""
            UPDATE account
            SET balance = balance - {amount}
            WHERE id = {id};
            """
  )

  cursor.execute(query)
  cursor.close()

  connection.commit()
  connection.close()

  # "fake" getting the new balance
  return current_bal - amount

# creates new account with inputted
# username and admin rights, hashed/salted password and 0 balance
# returns tuple of inputted row 
#  note: admin rights accepts 1/0 or true/false
# ({id}, {username}, {balance}, {is_admin})
# (assumes correct data types)
def create_account(username, password, is_admin):
  # normalize is_admin argument
  # to how it is needed in SQL
  if isinstance(is_admin, bool):
    is_admin = 1 if is_admin else 0

  password_hash = hash_salt(password)

  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  add_query = (f"""
                INSERT INTO account(username, password_hash, balance, is_admin)
                VALUES("{username}", {password_hash}, 0.00, {is_admin});
                """
  )

  # get the ID of the new account
  get_query = (f"""
               SELECT LAST_INSERT_ID();
               """
  )

  cursor.execute(add_query)
  cursor.execute(get_query)

  added_id = -1
  for item in cursor:
    added_id = item[0]

  cursor.close()

  connection.commit()
  connection.close()

  return (added_id, username, password_hash, 0.00, is_admin)

# deletes account with associated id
# returns account info if successfully deleted
# returns None if does not exist
def delete_account(id):
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  get_query = (f"""
                SELECT * FROM account
                WHERE id={id};
                """
  )

  rem_query = (f"""
               DELETE FROM account
               WHERE id={id};
               """
  )

  cursor.execute(get_query)

  # if no account was actually deleted
  if cursor.arraysize == 0:
    cursor.close()
    connection.close()
    return None

  del_account = None
  for item in cursor:
    del_account = item

  # return old account information 
  # (with the password hash in the correct form)
  ret = del_account[:2] + ('0x' + del_account[2].hex(),) + del_account[3:]
  
  cursor.execute(rem_query)
  cursor.close()

  connection.commit()
  connection.close()

  return ret

# given account id
# modifies username and/or password
# depending on what is given (defaults to None)
# if successful, returns NEW account
# else, returns None (also returns None if nothing set to change)
def modify_account(id, username=None, password=None):
  # if nothing is trying to be changed, don't bother
  if username is None and password is None:
    return None
  
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  get_query = (f"""
                SELECT * FROM account
                WHERE id={id};
                """
  )

  set_args = []

  if username is not None:
    set_args.append(f'username="{username}"')
  
  if password is not None:
    set_args.append(f'password_hash={hash_salt(password)}')

  # way to modularly choose what to set
  # and to what
  set_query = (f"""
               UPDATE account
               SET {', '.join(set_args)}
               WHERE id={id};
               """
  )

  cursor.execute(get_query)

  # if the account didn't exist
  if cursor.arraysize == 0:
    cursor.close()
    connection.close()
    return None

  old_account = None
  for item in cursor:
    old_account = item
  
  # "fake" re-getting the new information
  # adding comma turns middle element into tuple
  new_account = old_account[:1] + \
                ((username,) if username is not None else (old_account[1],)) + \
                ((hash_salt(password),) if password is not None else ('0x' + old_account[2].hex(),)) + \
                old_account[3:]

  cursor.execute(set_query)
  cursor.close()

  connection.commit()
  connection.close()

  return new_account

# for admins only
# returns list of tuples
# representing all accounts
# (except for password_hash)
def get_accounts():
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = (f"""
            SELECT id, username, balance, is_admin FROM account;
            """
  )

  cursor.execute(query)

  ret = []

  # get every detail except for password hash
  for item in cursor:
    ret.append((item[0], item[1], float(item[2]), item[3]))

  cursor.close()
  connection.close()

  return ret

# for admins only
# returns tuple of account (except password_hash) 
# given id
# if invalid id then returns None
def get_account(id):
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = (f"""
            SELECT id, username, balance, is_admin FROM account
            WHERE id={id};
            """
  )

  cursor.execute(query)

  ret = None

  # get every detail except for password hash
  for item in cursor:
    ret = (item[0], item[1], float(item[2]), item[3])

  cursor.close()
  connection.close()

  return ret

# for authentication, not ui
# takes username and returns list of all 
# (id, password hash) associated 
# if no accounts with that username, returns empty list
def get_credentials(username):
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = (f"""
            SELECT id, password_hash, is_admin FROM account
            WHERE username="{username}";
            """
  )

  cursor.execute(query)

  ret = []

  for item in cursor:
    ret.append((item[0], '0x' + item[1].hex(), item[2]))

  cursor.close()
  connection.close()

  return ret