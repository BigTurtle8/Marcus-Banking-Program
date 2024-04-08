import unittest
import mysql.connector
from dotenv import load_dotenv
import os
import random as rand
from sql_functions import check_balance, deposit, withdraw, create_account, delete_account, modify_account


class SQLTestCases(unittest.TestCase):
  def setUp(self):
    load_dotenv()

    self.connection = mysql.connector.connect( \
      user=os.environ.get('SQL_USER'), \
      database=os.environ.get('SQL_DATABASE'), \
      password=os.environ.get('SQL_PASSWORD'), \
    )

    self.cursor = self.connection.cursor()

  def test_create_delete_user_account(self):
    acc = create_account('Test Schmo', 0)
    self.assertEqual(acc[1:], ('Test Schmo', 0.0, 0))

    del_acc = delete_account(acc[0])
    self.assertEqual(acc, del_acc)

  def test_create_delete_admin_account(self):
    acc = create_account('Test Schmo', 1)
    self.assertEqual(acc[1:], ('Test Schmo', 0.0, 1))

    del_acc = delete_account(acc[0])
    self.assertEqual(acc, del_acc)

  def test_modify_account(self):
    orig_acc = create_account('Test Schmo', 0)
    mod_acc = modify_account(orig_acc[0], 'Test Schme')

    self.assertEqual(orig_acc[:1] + orig_acc[2:], mod_acc[:1] + mod_acc[2:])
    self.assertNotEqual(orig_acc[1], mod_acc[1])

    delete_account(orig_acc[0])

  def test_check_balance(self):
    acc = create_account('Test Schmo', 0)
    ret_bal = check_balance(acc[0])

    self.assertEqual(0, ret_bal)

    delete_account(acc[0])
    
  def test_deposit(self):
    acc = create_account('Test Schmo', 0)
    deposit(acc[0], (dep := rand.randrange(0, 100000)))

    self.assertEqual(dep, check_balance(acc[0]))

    delete_account(acc[0])

  def test_withdraw(self):
    acc = create_account('Test Schmo', 0)
    deposit(acc[0], (dep := rand.randrange(1000, 10000)))
    ret = withdraw(acc[0], (wit := rand.randrange(10, 900)))

    self.assertEqual(dep - wit, check_balance(acc[0]))
    self.assertEqual(dep - wit, ret)

    delete_account(acc[0])

  def test_withdraw_fail(self):
    acc = create_account('Test Schmo', 0)
    deposit(acc[0], (dep := rand.randrange(100, 900)))
    ret = withdraw(acc[0], (wit := rand.randrange(1000, 100000)))

    self.assertEqual(ret, dep - wit)
    self.assertEqual(dep, check_balance(acc[0]))

    delete_account(acc[0])

  def tearDown(self):
    self.cursor.close()
    self.connection.close()


if __name__ == '__main__':
  unittest.main()