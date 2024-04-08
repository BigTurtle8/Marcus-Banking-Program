import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def test():
  print(f'{check_balance(1):.2f}')
  print(f'{deposit(1, 100):.2f}')
  print(f'{withdraw(1, 2000):.2f}')

  created_account = create_account('Test Schmo', 0)
  print(f'{created_account}')
  print(f'{modify_account(created_account[0], 'Test Schme')}')
  print(f'{delete_account(created_account[0])}')

  print(f'{delete_account(-1)}')

# if account with id exists, will return float
# otherwise returns None
# (assumes correct data types)
def check_balance(id):
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  query = ("SELECT * FROM account;")

  cursor.execute(query)

  bal = None

  for item in cursor:
    item_id = item[0]

    if item_id == id:
      bal = item[2]

  cursor.close()
  connection.close()

  return bal

# if account with id exists, adds specified amount
# of money and returns NEW balance. 
# if doesn't exist, returns None
# (assumes correct data types)
def deposit(id, amount):
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

  return current_bal + amount

# if account with id exists, checks if enough money
#  if not enough, returns what the negative balance would've been
#  if is enough, removes that much money and returns NEW balance
# if account doesn't exist, returns None
# (assumes correct data types)
def withdraw(id, amount):
  current_bal = check_balance(id)
  
  if current_bal is None:
    return None
  
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

  return current_bal - amount

# creates new account with inputted
# username and admin rights and 0 balance
# returns tuple of inputted row 
#  note: admin rights accepts 1/0 or true/false
# ({id}, {username}, {balance}, {is_admin})
# (assumes correct data types)
def create_account(username, is_admin):
  if isinstance(is_admin, bool):
    is_admin = 1 if is_admin else 0

  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  add_query = (f"""
                INSERT INTO account(username, balance, is_admin)
                VALUES("{username}", 0.00, {is_admin});
                """
  )

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

  return (added_id, username, 0.00, is_admin)

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

  if cursor.arraysize == 0:
    cursor.close()
    connection.close()
    return None

  del_account = None
  for item in cursor:
    del_account = item
  
  cursor.execute(rem_query)
  cursor.close()

  connection.commit()
  connection.close()

  return del_account

# modifies account username
# given account id
# if successful, returns NEW account
# else, returns None
def modify_account(id, username):
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

  set_query = (f"""
               UPDATE account
               SET username="{username}"
               WHERE id={id};
               """
  )

  cursor.execute(get_query)

  if cursor.arraysize == 0:
    cursor.close()
    connection.close()
    return None

  old_account = None
  for item in cursor:
    old_account = item
  
  # adding comma turns middle element into typle
  new_account = old_account[:1] + (username,) + old_account[2:]

  cursor.execute(set_query)
  cursor.close()

  connection.commit()
  connection.close()

  return new_account