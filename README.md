# Turtle Banking

A rudimentary SQL-based banking app that allows for account balance manipulation as well as account modificaition.

## Running Locally

After cloning the repository onto the local machine, get a MySQL (or equivalent SQL provider) server locally running. On the SQL server, create a database. Then, run the equivalent of the following command (depicted below is for MySQL Workbench):

```SQL
CREATE TABLE `[database]`.`account` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password_hash` BINARY(32) NOT NULL,
  `balance` DECIMAL(18,2) NOT NULL,
  `is_admin` TINYINT NOT NULL,
  PRIMARY KEY (`id`));
```

Then, create a `.env` file with the following contents in the root folder of the banking program (in the same folder as `main.py`):

```
SQL_USER="[username]"
SQL_DATABASE="[database]"
SQL_PASSWORD="[password]"
```

Where:
- `[username]` is the SQL username.
- `[database]` is the name of the SQL database that the `account` table was created under.
- `[password]` is the password to this SQL server.

Finally, to ensure all the necessary dependencies are downloaded, run the following command in the root folder of the banking program:

```
pip install -r requirements.txt
```

## Credits
Made by Marcus A. for the Code2College Elite 102 course.