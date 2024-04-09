from hashlib import pbkdf2_hmac

# note: pbkdf2_hmac is hash and salt method for password
# hash_algo_iters increases security but also time
HASH_ITERS = 1000

SALT = b'\x02Y~\xdb&\xa8\xb0[-\xd8\xef\x82\x14\xc5f\xec'

# (have to add 0x for SQL)
def hash_salt(password):
  return '0x' + pbkdf2_hmac('sha256', str.encode(password), SALT, HASH_ITERS).hex()