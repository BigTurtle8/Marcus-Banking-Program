from backend.sql_functions import get_accounts, get_account, delete_account
from frontend.input_validation import val_get_account
from frontend.ui_utils import print_catastrophic_error

def do_admin_loop(id, username):
  while True:
    choice = ask_admin_menu(username)

    if not choice.isdigit():
      print_admin_error()
      continue

    match int(choice):
      case 1:
        do_see_loop()

      case 2: 
        do_delete_loop()

      case 3:
        break

      case _:
        print_admin_error()

def ask_admin_menu(username):
  print()
  print(f'Hello {username}. What would you like to do?')
  print('1. See accounts\n' +
        '2. Delete accounts\n' +
        '3. Exit\n')
  
  choice = input('Enter your choice (1-3) here: ')
  return choice

def print_admin_error():
  print()
  print('Sorry, that is not a valid input. Please enter 1, 2, or 3.')

def do_see_loop():
  print()
  print('Note: Admins listed as [ID#]A')
  print('---List of Accounts---')

  accounts = get_accounts()

  for (id, username, balance, is_admin) in accounts:
    print(f'{id}{'A' if is_admin == 1 else ''} - {username} (${balance:.2f})')

  print()
  input('> Enter anything to continue.')

def do_delete_loop():
  print()
  print('---Deleting Account---')

  account = None

  while True:
    id = input('Please enter account ID (Q to quit): ')

    if id.capitalize() == 'Q':
      return False

    if not id.isdigit():
      print('Not an integer id.')
      continue

    id = int(id)

    if not val_get_account(id) or (account := get_account(id)) is None:
      print('Not a valid id.')
      continue
    
    break

  print()
  print(f'---Account to be Deleted---')
  print(f'ID: {account[0]}')
  print(f'Username: {account[1]}')
  print(f'Balance: ${account[2]:.2f}')
  print(f'Admin: {'Yes' if account[3] == 1 else 'No'}')
  print(f'---------------------------')

  print()
  while True:
    choice = input('Would you like to delete this account (Y/N)? ')

    if choice.capitalize() == 'N':
      print()
      print('Deletion canceled.')
      
      print()
      input('> Enter anything to continue.')
      
      return False
    
    if choice.capitalize() == 'Y':
      if delete_account(account[0]) is None:
        print_catastrophic_error

      print()
      print(f'Account {id} has been deleted.')

      print()
      input('> Enter anything to continue.')

      return True
