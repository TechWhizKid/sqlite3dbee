import sqlite3
import click
import tabulate
import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

@click.group()
def cli():
    """Command-line interface for managing an SQLite database."""
    pass

# Function to create the database
@click.command()
@click.argument('filename', type=click.Path())
def mkdb(filename):
    """Create a new SQLite database file.

    Arg 1: FILENAME: Name of the SQLite database file to create.
    
    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        print(f"\nDatabase '{filename}' created successfully.")
    except sqlite3.Error as e:
        print(f"\nError creating database: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to create a table with specified columns (header)
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('columns', nargs=-1)
def adth(filename, columns):
    """Create a table with specified headers.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: [COLUMNS]: Tuple of column names.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the CREATE TABLE query
        create_table_query = f"CREATE TABLE IF NOT EXISTS data ({', '.join(columns)})"
        cursor.execute(create_table_query)
        connection.commit()

        print(f"\nTable header with columns {', '.join(columns)} created successfully.")
    except sqlite3.Error as e:
        print(f"\nError creating table header: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to add a new row of data
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('data', nargs=-1)
def adtd(filename, data):
    """Add a new row of data to the table.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: DATA: Data to be inserted as key-value pairs.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Parse the key-value pairs from data argument
        data_dict = dict(item.split(':') for item in data)

        # Insert the data into the table
        placeholders = ', '.join(['?' for _ in data_dict])
        insert_query = f"INSERT INTO data ({', '.join(data_dict.keys())}) VALUES ({placeholders})"
        cursor.execute(insert_query, list(data_dict.values()))
        connection.commit()

        print("\nA new row of data added successfully.")
    except sqlite3.Error as e:
        print(f"\nError adding row: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to modify a table header name
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('old_header_name')
@click.argument('new_header_name')
def mdth(filename, old_header_name, new_header_name):
    """Modify a table header name.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: OLD_HEADER_NAME: Current name of the table header.

    Arg 3: NEW_HEADER_NAME: New name for the table header.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Get the list of existing columns in the table
        cursor.execute(f"PRAGMA table_info(data)")
        columns = [column[1] for column in cursor.fetchall()]

        if old_header_name in columns:
            # Create a new table with the modified column name
            placeholders = ', '.join([f'{col} AS {new_header_name}' if col == old_header_name else col for col in columns])
            cursor.execute(f"CREATE TABLE data_temp AS SELECT {placeholders} FROM data")
            
            # Drop the old table
            cursor.execute("DROP TABLE data")
            
            # Rename the new table to the original table name
            cursor.execute("ALTER TABLE data_temp RENAME TO data")
            
            connection.commit()
            print(f"\nTable header name '{old_header_name}' changed to '{new_header_name}' successfully.")
        else:
            print(f"\nTable header '{old_header_name}' does not exist.")
    except sqlite3.Error as e:
        print(f"\nError modifying table header name: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to modify rows based on criteria
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('criteria')
@click.argument('new_data', nargs=-1)
def mdtd(filename, criteria, new_data):
    """Modify rows in the table based on criteria.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: CRITERIA: Criteria to match rows for modification.

    Arg 3: NEW_DATA: New data to update in the matching rows.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the UPDATE query
        update_query = f"UPDATE data SET {', '.join(new_data)} WHERE {criteria}"
        cursor.execute(update_query)
        connection.commit()

        print("\nRows modified successfully.")
    except sqlite3.Error as e:
        print(f"\nError modifying rows: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to search for data based on criteria
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('criteria', required=False)
def sctr(filename, criteria=None):
    """Search for rows in the table based on criteria.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: CRITERIA: Search criteria to match rows.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        if criteria:
            select_query = f"SELECT * FROM data WHERE {criteria}"
        else:
            select_query = "SELECT * FROM data"

        cursor.execute(select_query)
        rows = cursor.fetchall()

        if rows:
            headers = [desc[0] for desc in cursor.description]
            print(f"\n{tabulate.tabulate(rows, headers=headers)}")
        else:
            print("\nNo matching rows found.")
    except sqlite3.Error as e:
        print(f"\nError searching for rows: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to remove rows based on criteria
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('criteria')
def rmtr(filename, criteria):
    """Remove rows from the table based on criteria.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: CRITERIA: Criteria to match rows for removal.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the DELETE query
        delete_query = f"DELETE FROM data WHERE {criteria}"
        cursor.execute(delete_query)
        connection.commit()

        print("\nRow(s) removed successfully.")
    except sqlite3.Error as e:
        print(f"\nError removing rows: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to remove a table header and its data
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('header_name')
def rmtc(filename, header_name):
    """Remove a column from a table in the database.

    Arg 1: FILENAME: Name of the SQLite database file.

    Arg 2: HEADER_NAME: Name of the column to be removed.

    Note: Use command `xmpl` for usage example.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Get the list of table names in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table[0] for table in cursor.fetchall()]

        for table_name in table_names:
            # Check if the column exists in the current table
            cursor.execute(f"PRAGMA table_info({table_name})")
            table_info = cursor.fetchall()

            column_exists = any(col[1] == header_name for col in table_info)

            if column_exists:
                # Create a new table without the specified column
                create_table_query = f"CREATE TABLE new_{table_name} AS SELECT "
                columns = [col[1] for col in table_info if col[1] != header_name]
                create_table_query += ', '.join(columns) + f" FROM {table_name}"

                cursor.execute(create_table_query)
                connection.commit()

                # Drop the old table
                cursor.execute(f"DROP TABLE {table_name}")
                connection.commit()

                # Rename the new table to the original table name
                cursor.execute(f"ALTER TABLE new_{table_name} RENAME TO {table_name}")
                connection.commit()

                print(f"\nColumn '{header_name}' removed from table '{table_name}' successfully.")
            else:
                print(f"\nColumn '{header_name}' does not exist in table '{table_name}'.")

    except sqlite3.Error as e:
        print(f"\nError removing column: {str(e)}")
    finally:
        if connection:
            connection.close()

def derive_key_from_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32
    )
    key = kdf.derive(password.encode())
    return key

# Function to encrypt database
@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('password', type=str)
@click.argument('confirm_password', type=str)
def lkdb(file_path, password, confirm_password):
    """Lock the SQLite database with encryption.

    Arg 1: FILE_PATH: Name of the SQLite database file.

    Arg 2: PASSWORD: Encryption password.

    Arg 3: CONFIRM_PASSWORD: Confirmation of encryption password.

    Note: Use command `xmpl` for usage example.
    """
    if password != confirm_password:
        print("Password and confirmation password do not match.")
        return

    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()

        salt = os.urandom(16)  # Generate a random salt
        key = derive_key_from_password(password, salt)

        fernet = Fernet(base64.urlsafe_b64encode(key))
        encrypted_data = fernet.encrypt(file_data)

        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(salt + encrypted_data)

        print(f"\nFile '{file_path}' is now locked and cannot be read or modified.")
    except Exception as e:
        print(f"\nError encrypting file: {str(e)}")

# Function to decrypt database
@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('password', type=str)
def ukdb(file_path, password):
    """Unlock the SQLite database with decryption.

    Arg 1: FILE_PATH: Name of the SQLite database file.

    Arg 2: PASSWORD: Decryption password.

    Note: Use command `xmpl` for usage example.
    """
    try:
        with open(file_path, 'rb') as encrypted_file:
            file_data = encrypted_file.read()

        salt = file_data[:16]  # Read the salt from the file
        encrypted_data = file_data[16:]  # Read the encrypted data from the file

        key = derive_key_from_password(password, salt)

        fernet = Fernet(base64.urlsafe_b64encode(key))
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_path, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_data)

        print(f"\nFile '{file_path}' is unlocked and can now be read and modified.")
    except Exception as e:
        print(f"\nError decrypting file: {str(e)}")

# Just a help menu
@click.command()
def help():
    """Shows a help message that is actually helpful."""
    print(f"\nUsage: {os.path.basename(__file__)} [OPTIONS] [COMMAND] <filename> [ARGS]")
    print(f"\n  Command-line interface for managing an SQLite database.")
    print(f"\nOptions:")
    print(f"  --help Show help message and exit.")
    print(f"\nCommands:")
    print(f"  mkdb  Create a new SQLite database file.")
    print(f"  adth  Create a table with specified headers.")
    print(f"  adtd  Add a new row of data to the table.")
    print(f"  mdth  Modify a table header name.")
    print(f"  mdtd  Modify rows in the table based on criteria.")
    print(f"  sctr  Search for rows in the table based on criteria.")
    print(f"  rmtr  Remove rows from the table based on criteria.")
    print(f"  rmtc  Remove a column from a table in the database.")
    print(f"  lkdb  Lock the SQLite database with encryption.")
    print(f"  ukdb  Unlock the SQLite database with decryption.")
    print(f"  help  Show this message and exit.")
    print(f"  xmpl  Shows a help message with usage example.")

@click.command()
def xmpl():
    """Shows a help message with usage example."""
    appname = os.path.basename(__file__)
    print(f"\nUsage: {appname} [COMMAND] <filename> [ARGS]")
    print(f"\n  Command-line interface for managing an SQLite database.")
    print(f"\nAvailable commands: # Use command 'help' or option '--help' for more info.")
    print(f"  mkdb, adth, adtd, mdth, mdtd, sctr, rmtr, rmtc, lkdb, ukdb, help and xmpl.")
    print(f"\nCommand usage:")
    print(f"  {appname} mkdb <filename>")
    print(f"  {appname} adth <filename> \"TH_1\" \"TH_2\" \"TH_3\"...")
    print(f"  {appname} adtd <filename> \"TH_1\":\"DATA_1\" \"TH_2\":\"DATA_2\" \"TH_3\":\"DATA_3\"...")
    print(f"  {appname} mdth <filename> \"TH_3\" \"TH_4\"")
    print(f"  {appname} mdtd <filename> \"TH_4 = \'DATA_3\'\" \"TH_4 = \'DATA_4\'\"")
    print(f"  {appname} sctr <filename> \"TH_2 = \'DATA_2\'\"")
    print(f"  {appname} rmtr <filename> \"TH_2 = \'DATA_2\'\"")
    print(f"  {appname} rmtc <filename> \"TH_4\"")
    print(f"  {appname} lkdb <filename> <password> <confirm_password>")
    print(f"  {appname} ukdb <filename> <password>")
    print(f"\nCommand examples:")
    print(f"  {appname} mkdb database.sql")
    print(f"  {appname} adth database.sql \"Name\" \"Age\" \"UserName\" \"UserID\"")
    print(f"  {appname} adtd database.sql \"Name\":\"Robby Russel\" \"Age\":\"25\" \"UserName\":\"robby_fr\" \"UserID\":\"1029384756\"")
    print(f"  {appname} mdth database.sql \"Name\" \"RealName\"")
    print(f"  {appname} mdtd database.sql \"Age = \'25\'\" \"Age = \'26\'\"")
    print(f"  {appname} sctr database.sql \"Age = \'26\'\"")
    print(f"  {appname} rmtr database.sql \"UserName = \'robby_fr\'\"")
    print(f"  {appname} rmtc database.sql \"UserName\"")
    print(f"  {appname} lkdb database.sql \"123456\" \"123456\"")
    print(f"  {appname} ukdb database.sql \"123456\"")

# Add commands to the click CLI
cli.add_command(mkdb, name='mkdb')
cli.add_command(adth, name='adth')
cli.add_command(adtd, name='adtd')
cli.add_command(mdth, name='mdth')
cli.add_command(mdtd, name='mdtd')
cli.add_command(sctr, name='sctr')
cli.add_command(rmtr, name='rmtr')
cli.add_command(rmtc, name='rmtc')
cli.add_command(lkdb, name='lkdb')
cli.add_command(ukdb, name='ukdb')
cli.add_command(help, name='help')
cli.add_command(xmpl, name='xmpl')

# Run the CLI
if __name__ == '__main__':
    cli()
