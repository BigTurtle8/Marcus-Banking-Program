def main():
  print('Welcome to Turtle Banking!')
  
  do_main_loop()
    
def do_main_loop():
  while True:
    main_choice = ask_main_menu()

    if not main_choice.isdigit():
      print_main_error()
      continue

    match int(main_choice): 
      case 1:
        print('Logging in...')

      case 2:
        print('Signing up...')

      case 3:
        print_exit_message()
        break

      case _:
        print_main_error()

def ask_main_menu():
  print('What would you like to do?')
  print('1. Log in\n' +
        '2. Sign up\n' +
        '3. Exit\n')
  
  choice = input('Enter your choice (1-3) here: ')
  return choice

def print_main_error():
  print()
  print('Sorry, that is not a valid input. Please enter 1, 2, or 3.')
  print()

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
