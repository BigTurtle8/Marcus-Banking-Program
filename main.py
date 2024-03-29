def main():
  print('Welcome to Turtle Banking!')
  
  do_main_loop()
    
def do_main_loop():
  while True:
    choice = ask_main_menu()

    if not choice.isdigit():
      print_main_error()
      continue

    match int(choice): 
      case 1:
        do_login_loop()

      case 2:
        # To be implemented later
        print('Signing up...')

      case 3:
        print_exit_message()
        break

      case _:
        print_main_error()

def ask_main_menu():
  print()
  print('What would you like to do?')
  print('1. Log in\n' +
        '2. Sign up\n' +
        '3. Exit\n')
  
  choice = input('Enter your choice (1-3) here: ')
  return choice

def print_main_error():
  print()
  print('Sorry, that is not a valid input. Please enter 1, 2, or 3.')

def do_login_loop():
  while True:
    choice = ask_login_menu()

    if not choice.isdigit():
      print_login_error()
      continue

    match int(choice):
      case 1:
        print('User')

      case 2: 
        print('Admin')

      case 3:
        break

      case _:
        print_login_error()

def ask_login_menu():
  print()
  print('Who are you logging in as?')
  print('1. User\n' +
        '2. Administrator\n' +
        '3. Exit\n')
  
  choice = input('Enter your choice (1-3) here: ')
  return choice

def print_login_error():
  print()
  print('Sorry, that is not a valid input. Please enter 1, 2, or 3.')

def print_exit_message():
  print()
  print('|' + '-' * 37 + '|')
  print('|' + ' ' * 37 + '|')
  print('| Thank you for using Turtle Banking. |')
  print('|' + ' ' * 37 + '|')
  print('|' + '-' * 37 + '|')
  print()

if __name__ == '__main__':
  main()
