from backend.sql_functions import get_credentials
from backend.utils import hash_salt

# takes in strings of username and password
# and if account exists, returns corresponding id
# if account exists but incorrect password, returns -1
# if account does not exist, returns None
# note: expects username and password to be reasonable length
# (<1024 characters)
def authenticate(username, password):
  password_hash = hash_salt(password)
  hashes = get_credentials(username)

  if len(hashes) == 0:
    return None
  
  for id, hash, is_admin in hashes:
    if hash == password_hash:
      return (id, is_admin)
    
  return -1
