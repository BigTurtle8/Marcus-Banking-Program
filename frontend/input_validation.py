# helper methods to for ui.py to use before inputting sql_functions.py
# ONLY checks argument types, not if works with database (already done in sql_functions.py)

# checks if id is int that is at least 1
# returns true if OK, else false
def val_check_balance(id):
  if not isinstance(id, int) or id <= 0:
    return False

  return True

# checks if id is int that is at least 1
# and if amount is positive decimal / int
# returns true if OK, else false
def val_deposit(id, amount):
  if not isinstance(id, int) or id <= 0:
    return False
  
  if not isinstance(amount, (int, float)) or amount < 0:
    return False
  
  return True

# checks if id is int that is at least 1
# and if amount is positive decimal / int
# returns true if OK, else false
def val_withdraw(id, amount):
  if not isinstance(id, int) or id <= 0:
    return False
  
  if not isinstance(amount, (int, float)) or amount < 0:
    return False
  
  return True

# checks if username is string,
# and if password is string,
# and if is_admin 1/0 or true/false
# returns true if OK, else false
def val_create_account(username, password, is_admin):
  if not isinstance(username, str):
    return False
  
  if not isinstance(password, str):
    return False
  
  if isinstance(is_admin, int):
    if is_admin in [0, 1]:
      return True

    else:
      return False
        
  if not isinstance(is_admin, bool):
    return False
  
  return True

# checks if id is int that is at least 1
# returns true if OK, else false
def val_delete_account(id):
  if not isinstance(id, int) or id <= 0:
    return False
  
  return True

# checks if id is int that is at least 1
# and if username is string,
# and if password is string,
# returns true if OK, else false
def val_modify_account(id, username=None, password=None):
  if not isinstance(id, int) or id <= 0:
    return False
  
  if username is not None and not isinstance(username, str):
    return False
  
  if password is not None and not isinstance(password, str):
    return False
  
  return True

def val_get_account(id):
  if not isinstance(id, int) or id <= 0:
    return False

  return True
