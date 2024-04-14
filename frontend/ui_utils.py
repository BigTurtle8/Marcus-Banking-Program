def print_catastrophic_error():
  print()
  print('-' * 20)
  print('Something went very wrong. Please report this to an admin at your earliest convenience.')
  print('-' * 20)
  print()

def is_number(num):
  try:
    float(num)
    return True
  
  except ValueError:
    return False