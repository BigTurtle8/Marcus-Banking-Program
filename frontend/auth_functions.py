from backend.authentication import authenticate
from backend.sql_functions import create_account
from frontend.user_functions import do_user_loop
from frontend.admin_functions import do_admin_loop
from frontend.input_validation import val_create_account
from frontend.ui_utils import print_catastrophic_error

def do_login_loop():
  while True:
    print()
    print('---Logging In---')
    username = input('Username: ')
    password = input('Password: ')

    ret_auth = authenticate(username, password)

    if ret_auth is None or ret_auth == -1:
      print()
      print('> INCORRECT username or password. <')
      return False
    
    id, is_admin = ret_auth

    if is_admin == 0:
      do_user_loop(id, username)
      break

    elif is_admin == 1:
      do_admin_loop(id, username)
      break

# assumes is regular user; for an admin account have to add directly in SQL
def do_signup_loop():
  print()
  print('---Creating Account---')
  username = password = None

  while username is None:
    username = input('Enter a username: ')

  while password is None:
    password = input('Enter a password: ')

  while True:
    check = input('Please re-enter your password (Q to quit): ')

    if check.capitalize() == 'Q':
      return False

    if check == password:
      break

    print('That is not correct. Try again (Q to quit).')

  print()
  print('Does this look correct?')
  print(f'---Pending Account---\n'
        f'Username: {username}\n'
        f'Password: {'*' * len(password)}\n'
        f'---------------------'
  )

  while True:
    choice = input('Enter Y/N here: ')

    if choice.capitalize() == 'N':
      print('Account creation canceled.')
      return False
    
    if choice.capitalize() == 'Y':
      if val_create_account(username, password, 0):
        return create_account(username, password, 0) 

      else:
        print_catastrophic_error()

