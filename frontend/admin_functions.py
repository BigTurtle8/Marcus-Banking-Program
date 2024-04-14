def do_admin_loop():
  while True:
    choice = ask_admin_menu()

    if not choice.isdigit():
      print_admin_error()
      continue

    match int(choice):
      case 1:
        # To be implemented later
        print('Seeing accounts...')

      case 2: 
        # To be implemented later
        print('Deleting accounts...')

      case 3:
        break

      case _:
        print_admin_error()

def ask_admin_menu():
  print()
  print('Who are you logging in as?')
  print('1. See accounts\n' +
        '2. Delete accounts\n' +
        '3. Exit\n')
  
  choice = input('Enter your choice (1-3) here: ')
  return choice

def print_admin_error():
  print()
  print('Sorry, that is not a valid input. Please enter 1, 2, or 3.')