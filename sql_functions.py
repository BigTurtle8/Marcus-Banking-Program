import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def test():
  connection = mysql.connector.connect( \
    user=os.environ.get('SQL_USER'), \
    database=os.environ.get('SQL_DATABASE'), \
    password=os.environ.get('SQL_PASSWORD'), \
  )

  cursor = connection.cursor()

  test_query = ("SELECT * FROM student")

  cursor.execute(test_query)

  for item in cursor:
    print(item)

  connection.close()