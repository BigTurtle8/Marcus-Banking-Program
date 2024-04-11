import unittest
import mysql.connector
from dotenv import load_dotenv
import os
import random as rand
from frontend.input_validation import val_check_balance, val_deposit, val_withdraw, val_create_account, val_delete_account, val_modify_account
from backend.sql_functions import check_balance, deposit, withdraw, create_account, delete_account, modify_account, get_credentials
from backend.authentication import authenticate
from backend.utils import hash_salt

class ValidationTestCases(unittest.TestCase):
  def test_val_check_balance(self):
    self.assertFalse(val_check_balance(-1))
    self.assertFalse(val_check_balance(0))
    self.assertFalse(val_check_balance(rand.randrange(-10000, 0)))
    
    self.assertTrue(val_check_balance(1))
    self.assertTrue(val_check_balance(rand.randrange(2, 10000)))

  def test_val_deposit(self):
    self.assertFalse(val_deposit(-1, 1))
    self.assertFalse(val_deposit(0, 1))
    
    self.assertFalse(val_deposit(rand.randrange(-10000, 0), 1))
    
    self.assertTrue(val_deposit(1, 1))
    self.assertTrue(val_deposit(rand.randrange(2, 10000), 1))

    self.assertFalse(val_deposit(1, -1))
    self.assertFalse(val_deposit(1, rand.randrange(-10000, -1)))

    self.assertTrue(val_deposit(1, 1))
    self.assertTrue(val_deposit(1, 0))
    self.assertTrue(val_deposit(rand.randrange(1, 10000), rand.randrange(0, 10000)))

    self.assertFalse(val_deposit(1, -0.5))
    self.assertTrue(val_deposit(1, 0.5))

  def test_val_withdraw(self):
    self.assertFalse(val_withdraw(-1, 1))
    self.assertFalse(val_withdraw(0, 1))
    
    self.assertFalse(val_withdraw(rand.randrange(-10000, 0), 1))
    
    self.assertTrue(val_withdraw(1, 1))
    self.assertTrue(val_withdraw(rand.randrange(2, 10000), 1))

    self.assertFalse(val_withdraw(1, -1))
    self.assertFalse(val_withdraw(1, rand.randrange(-10000, -1)))

    self.assertTrue(val_withdraw(1, 1))
    self.assertTrue(val_withdraw(1, 0))
    self.assertTrue(val_withdraw(rand.randrange(1, 10000), rand.randrange(0, 10000)))

    self.assertFalse(val_withdraw(1, -0.5))
    self.assertTrue(val_withdraw(1, 0.5))

  def test_val_create_account(self):
    self.assertFalse(val_create_account(1, 'password123*', 0))

    self.assertFalse(val_create_account('Test Schmo', 1, 0))

    self.assertFalse(val_create_account('Test Schmo', 'password123*', 'user'))
    self.assertFalse(val_create_account('Test Schmo', 'password123*', 2))
    self.assertFalse(val_create_account('Test Schmo', 'password123*', 1.0))

    self.assertTrue(val_create_account('Test Schmo', 'password123*', 0))
    self.assertTrue(val_create_account('Test Schmo', 'password123*', 1))
    self.assertTrue(val_create_account('Test Schmo', 'password123*', True))
    self.assertTrue(val_create_account('Test Schmo', 'password123*', False))
    
  def test_val_delete_account(self):
    self.assertFalse(val_delete_account(-1))
    self.assertFalse(val_delete_account(0))
    self.assertFalse(val_delete_account(rand.randrange(-10000, 0)))
    
    self.assertTrue(val_delete_account(1))
    self.assertTrue(val_delete_account(rand.randrange(2, 10000)))

  def test_val_modify_account(self):
    self.assertFalse(val_modify_account(-1, 'Test Schmo', 'password123*'))
    self.assertFalse(val_modify_account(0, 'Test Schmo', 'password123*'))
    self.assertFalse(val_modify_account(-1, 'Test Schmo'))
    self.assertFalse(val_modify_account(0, 'Test Schmo'))
    self.assertFalse(val_modify_account(-1, username='Test Schmo'))
    self.assertFalse(val_modify_account(0, username='Test Schmo'))
    self.assertFalse(val_modify_account(-1, password='password123*'))
    self.assertFalse(val_modify_account(0, password='password123*'))

    self.assertFalse(val_modify_account(1, 1, 'password123*'))
    self.assertFalse(val_modify_account(1, 1))
    self.assertFalse(val_modify_account(1, username=1))

    self.assertFalse(val_modify_account(1, 'Test Schmo', 1))
    self.assertFalse(val_modify_account(1, password=1))

    self.assertTrue(val_modify_account(1, 'Test Schmo', 'password123*'))
    self.assertTrue(val_modify_account(1, 'Test Schmo'))
    self.assertTrue(val_modify_account(1, username='Test Schmo'))
    self.assertTrue(val_modify_account(1, password='password123*'))

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
    acc = create_account('Test Schmo', 'password123*', 0)
    self.assertEqual(acc[1:], ('Test Schmo', hash_salt('password123*'), 0.0, 0))

    del_acc = delete_account(acc[0])
    self.assertEqual(acc, del_acc)

  def test_create_delete_admin_account(self):
    acc = create_account('Test Schmo', 'password123*', 1)
    self.assertEqual(acc[1:], ('Test Schmo', hash_salt('password123*'), 0.0, 1))

    del_acc = delete_account(acc[0])
    self.assertEqual(acc, del_acc)

  def test_modify_account(self):
    orig_acc = create_account('Test Schmo', 'password123*', 0)
    mod_1_acc = modify_account(orig_acc[0], username='Test Schme')

    self.assertEqual(orig_acc[:1] + orig_acc[2:], mod_1_acc[:1] + mod_1_acc[2:])
    self.assertNotEqual(orig_acc[1], mod_1_acc[1])

    mod_2_acc = modify_account(orig_acc[0], password='password234*')
    self.assertEqual(mod_1_acc[:2] + mod_1_acc[3:], mod_2_acc[:2] + mod_2_acc[3:])
    self.assertNotEqual(mod_1_acc[2], mod_2_acc[2])

    mod_3_acc = modify_account(orig_acc[0], username='Test Schma', password='password345*')
    self.assertEqual(mod_2_acc[:1] + mod_2_acc[3:], mod_3_acc[:1] + mod_3_acc[3:])
    self.assertNotEqual(mod_2_acc[1], mod_3_acc[1])
    self.assertNotEqual(mod_2_acc[2], mod_3_acc[2])

    mod_4_acc = modify_account(orig_acc[0])
    self.assertIsNone(mod_4_acc)

    delete_account(orig_acc[0])

  def test_check_balance(self):
    acc = create_account('Test Schmo', 'password123*', 0)
    ret_bal = check_balance(acc[0])

    self.assertEqual(0, ret_bal)

    delete_account(acc[0])
    
  def test_deposit(self):
    acc = create_account('Test Schmo', 'password123*', 0)
    deposit(acc[0], (dep := rand.randrange(0, 100000)))

    self.assertEqual(dep, check_balance(acc[0]))

    delete_account(acc[0])

  def test_withdraw(self):
    acc = create_account('Test Schmo', 'password123*', 0)
    deposit(acc[0], (dep := rand.randrange(1000, 10000)))
    ret = withdraw(acc[0], (wit := rand.randrange(10, 900)))

    self.assertEqual(dep - wit, check_balance(acc[0]))
    self.assertEqual(dep - wit, ret)

    delete_account(acc[0])

  def test_withdraw_fail(self):
    acc = create_account('Test Schmo', 'password123*', 0)
    deposit(acc[0], (dep := rand.randrange(100, 900)))
    ret = withdraw(acc[0], (wit := rand.randrange(1000, 100000)))

    self.assertEqual(ret, dep - wit)
    self.assertEqual(dep, check_balance(acc[0]))

    delete_account(acc[0])

  def test_get_credentials(self):
    acc = create_account('Test Schmo', 'password123*', 0)
    
    ret = get_credentials('Test Schmo')

    self.assertEqual([(acc[0], acc[2])], ret)

    delete_account(acc[0])

  def tearDown(self):
    self.cursor.close()
    self.connection.close()


class AutheticationTestCases(unittest.TestCase):
  def setUp(self):
    self.acc1 = create_account('Test Schmo', 'password123*', 0)
    self.acc2 = create_account('Test Schme', 'password234*', 0)
    self.acc3 = create_account('Test Schma', 'password123*', 0)
    self.acc4 = create_account('Test Schmo', 'password234*', 0)

  def test_correct_auth(self):
    ret = authenticate('Test Schmo', 'password123*')

    self.assertEqual(ret, self.acc1[0])

  def test_incorrect_auth(self):
    ret = authenticate('Test Schme', 'password123*')

    self.assertEqual(ret, -1)

  def test_auth_user_collision(self):
    ret1 = authenticate('Test Schmo', 'password123*')
    ret2 = authenticate('Test Schmo', 'password234*')

    self.assertEqual(ret1, self.acc1[0])
    self.assertEqual(ret2, self.acc4[0])

  def test_auth_pass_collision(self):
    ret1 = authenticate('Test Schmo', 'password123*')
    ret2 = authenticate('Test Schma', 'password123*')

    self.assertEqual(ret1, self.acc1[0])
    self.assertEqual(ret2, self.acc3[0])

  def tearDown(self):
    delete_account(self.acc1[0])
    delete_account(self.acc2[0])
    delete_account(self.acc3[0])
    delete_account(self.acc4[0])


if __name__ == '__main__':
  unittest.main()
