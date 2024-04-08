import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def test():
  print(f'{check_balance(1):.2f}')
  print(f'{deposit(100, 1):.2f}')
  print(f'{withdraw(2000, 1):.2f}')

# if account with id exists, will return float
# otherwise returns None
def check_balance(id):
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  test_query = ("SELECT * FROM account;")

  cursor.execute(test_query)

  ret = None

  for item in cursor:
    item_id = item[0]

    if item_id == id:
      ret = item[2]

  cursor.close()
  connection.close()

  return ret

# if account with id exists, adds specified amount
# of money and returns NEW balance. 
# if doesn't exist, returns None
# (assumes correct data types)
def deposit(amount, id):
  current_bal = check_balance(id)
  
  if current_bal is None:
    return None

  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  test_query = (f"""
                UPDATE account
                SET balance = balance + {amount}
                WHERE id = {id};
                """
  )

  cursor.execute(test_query)
  cursor.close()

  # REALLY IMPORTANT TO COMMIT
  connection.commit()
  connection.close()

  return current_bal + amount

# if account with id exists, checks if enough money
#  if not enough, returns what the negative balance would've been
#  if is enough, removes that much money and returns NEW balance
# if account doesn't exist, returns None
def withdraw(amount, id):
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

  test_query = (f"""
                UPDATE account
                SET balance = balance - {amount}
                WHERE id = {id};
                """
  )

  cursor.execute(test_query)
  cursor.close()

  # REALLY IMPORTANT TO COMMIT
  connection.commit()
  connection.close()

  return current_bal - amount