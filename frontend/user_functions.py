from backend.sql_functions import check_balance, deposit, withdraw, modify_account, delete_account
from backend.authentication import authenticate
from frontend.input_validation import val_check_balance, val_deposit, val_withdraw, val_modify_account, val_delete_account
from frontend.ui_utils import print_catastrophic_error, is_number

def do_user_loop(id, username):
  while True:
    choice = ask_user_menu(username)

    if not choice.isdigit():
      print_user_error()
      continue

    match int(choice):
      case 1:
        do_check_balance_loop(id)

      case 2:
        do_deposit_loop(id)

      case 3:
        do_withdraw_loop(id)

      case 4:
        new_account = do_modify_loop(id, username)

        if not isinstance(new_account, bool): 
          id, username = new_account[0:2]

      case 5:
        if do_delete_loop(id, username):
          break

      case 6:
        break

      case _:
        print_user_error()

def ask_user_menu(username):
  print()
  print(f'Hello {username}. What would you like to do?')
  print('1. Check balance\n' +
        '2. Deposit\n' +
        '3. Withdraw\n' +
        '4. Modify account\n' +
        '5. Delete account\n' +
        '6. Log out\n')
  
  choice = input('Enter your choice (1-6) here: ')
  return choice

def print_user_error():
  print()
  print('Sorry, that is not a valid input. Please enter 1, 2, 3, 4, 5, or 6.')

def do_check_balance_loop(id):
  print()
  print('---Current Balance---')

  if not val_check_balance(id) or (bal := check_balance(id)) is None:
    print_catastrophic_error()
    return False
  
  print(f'${float(bal):,.2f}')

  print()
  input('> Enter anything to continue.')

def do_deposit_loop(id):
  print()
  print('---Depositing---')

  while True:
    amt = input('Please enter how much you would like to deposit: ')

    if not is_number(amt) or float(amt) < 0:
      print('Please enter a positive numerical value (10 or 10.0, not $10).')
      continue
      
    amt = round(float(amt), 2)

    print()
    while True: 
      choice = input(f'Depositing ${amt:,.2f}. Is this correct (Y/N)? ')

      if choice.capitalize() == 'N':
        print('Deposit canceled.')

        print()
        input('> Enter anything to continue.')
        break

      if choice.capitalize() == 'Y':
        print('Proceeding with deposit...')
        
        if not val_deposit(id, amt) or (ret := deposit(id, amt)) is None:
          print_catastrophic_error()
          break

        print()
        print(f'New Balance: ${ret:,.2f}')

        print()
        input('> Enter anything to continue.')

        break
    
    break


def do_withdraw_loop(id):
  print()
  print('---Withdrawing---')

  while True:
    amt = input('Please enter how much you would like to withdraw: ')

    if not is_number(amt) or float(amt) < 0:
      print('Please enter a positive numerical value (10 or 10.0, not $10).')
      continue
      
    amt = round(float(amt), 2)

    print()
    while True: 
      choice = input(f'Withdrawing ${amt:,.2f}. Is this correct (Y/N)? ')

      if choice.capitalize() == 'N':
        print('Withdrawal canceled.')

        print()
        input('> Enter anything to continue.')
        break

      if choice.capitalize() == 'Y':
        print('Proceeding with withdrawal...')
        
        if not val_withdraw(id, amt) or (ret := withdraw(id, amt)) is None:
          print_catastrophic_error()
          break

        if ret < 0:
          print('Insufficient funds. Withdrawal automatically canceled.')

        else:
          print()
          print(f'New Balance: ${ret:,.2f}')

        print()
        input('> Enter anything to continue.')

        break
    
    break

def do_modify_loop(id, username):
  print()
  print('---Modifying Account---')
  print('To ensure your identity, please re-enter your password.')
  password = input('Enter password: ')

  if (ret_auth := authenticate(username, password)) is None or ret_auth == -1 or ret_auth[0] != id:
    print()
    print('Incorrect password.')
    print('Modification canceled.')

    print()
    input('> Enter anything to continue.')
    
    return False
  
  print()
  new_username = input('Please enter your new username: ')
  new_password = input('Please enter your new password: ')

  print()
  print(f'---Pending Changes---')
  print(f'Username: {new_username}')
  print(f'Password: {'*' * len(new_password)}')
  print(f'---------------------')

  while True:
    print()
    print('Does this look correct?')
    choice = input('Enter Y/N here: ')

    if choice.capitalize() == 'N':
      print('Account modification canceled.')
      return False
    
    if choice.capitalize() == 'Y':
      if val_modify_account(id, new_username, new_password):
        return modify_account(id, new_username, new_password) 

      else:
        print_catastrophic_error()

def do_delete_loop(id, username):
  print()
  print('---Deleting Account---')
  print('To ensure your identity, please re-enter your password.')
  password = input('Enter password (enter anything to cancel): ')

  if (ret_auth := authenticate(username, password)) is None or ret_auth == -1 or ret_auth[0] != id:
    print()
    print('Incorrect password.')
    print('Deletion canceled.')

    print()
    input('> Enter anything to continue.')
    
    return False

  print()
  print('After you delete your account, there is NO way to recover it.')
  print('To confirm you understand and completely delete your account, re-enter your password.')
  conf_password = input('Enter password (enter anything to cancel): ')

  if conf_password != password:
    print()
    print('Incorrect password.')
    print('Deletion canceled.')

    print()
    input('> Enter anything to continue.')
    
    return False

  if not val_delete_account(id) or delete_account(id) is None:
    print_catastrophic_error()
    return False
  
  print()
  print('Your account has been deleted.')

  print()
  input('> Enter anything to continue.')

  return True
