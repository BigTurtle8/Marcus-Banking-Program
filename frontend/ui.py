from backend.sql_functions import *
from frontend.input_validation import *
from frontend.auth_functions import do_login_loop, do_signup_loop

'''
Only has a Command Line Interface for now.
Provides the beginning and start of user experience.
'''

def run():
  print('|' + '-' * 28 + '|')
  print('|' + ' ' * 28 + '|')
  print('| Welcome to Turtle Banking! | ')
  print('|' + ' ' * 28 + '|')
  print('|' + '-' * 28 + '|')

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
        do_signup_loop()

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

def print_exit_message():
  print()
  print('|' + '-' * 37 + '|')
  print('|' + ' ' * 37 + '|')
  print('| Thank you for using Turtle Banking. |')
  print('|' + ' ' * 37 + '|')
  print('|' + '-' * 37 + '|')
  print()
