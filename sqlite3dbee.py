import sqlite3
import click
import tabulate
import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Function to create the database
@click.command()
@click.argument('filename', type=click.Path())
def make_database(filename):
    """Create a new SQLite database file.

    Args:
        filename (str): Name of the SQLite database file.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        print(f"Database '{filename}' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating database: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to create a table with specified columns (header)
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('columns', nargs=-1)
def insert_table_header(filename, columns):
    """Create a table with specified headers.

    Args:
        filename (str): Name of the SQLite database file.
        columns (tuple): Tuple of column names.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the CREATE TABLE query
        create_table_query = f"CREATE TABLE IF NOT EXISTS data ({', '.join(columns)})"
        cursor.execute(create_table_query)
        connection.commit()

        print(f"Table header with columns {', '.join(columns)} created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table header: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to add a new row of data
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('data', nargs=-1)
def add_table_data(filename, data):
    """Add a new row of data to the table.

    Args:
        filename (str): Name of the SQLite database file.
        data (tuple): Data to be inserted as key-value pairs.
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

        print("A new row of data added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding row: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to search for data based on criteria
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('criteria', required=False)
def search_data(filename, criteria=None):
    """Search for rows in the table based on criteria.

    Args:
        filename (str): Name of the SQLite database file.
        criteria (str, optional): Search criteria to match rows.
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
            print(tabulate.tabulate(rows, headers=headers))
        else:
            print("No matching rows found.")
    except sqlite3.Error as e:
        print(f"Error searching for rows: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to remove rows based on criteria
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('criteria')
def remove_data(filename, criteria):
    """Remove rows from the table based on criteria.

    Args:
        filename (str): Name of the SQLite database file.
        criteria (str): Criteria to match rows for removal.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the DELETE query
        delete_query = f"DELETE FROM data WHERE {criteria}"
        cursor.execute(delete_query)
        connection.commit()

        print("Row(s) removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing rows: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to modify rows based on criteria
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('criteria')
@click.argument('new_data', nargs=-1)
def modify_data(filename, criteria, new_data):
    """Modify rows in the table based on criteria.

    Args:
        filename (str): Name of the SQLite database file.
        criteria (str): Criteria to match rows for modification.
        new_data (tuple): New data to update in the matching rows.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the UPDATE query
        update_query = f"UPDATE data SET {', '.join(new_data)} WHERE {criteria}"
        cursor.execute(update_query)
        connection.commit()

        print("Rows modified successfully.")
    except sqlite3.Error as e:
        print(f"Error modifying rows: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to remove a table header and its data
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('header_name')
def remove_table_header(filename, header_name):
    """Remove a column from a table in the database.

    Args:
        filename (str): Name of the SQLite database file.
        header_name (str): Name of the column to be removed.
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

                print(f"Column '{header_name}' removed from table '{table_name}' successfully.")
            else:
                print(f"Column '{header_name}' does not exist in table '{table_name}'.")

    except sqlite3.Error as e:
        print(f"Error removing column: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to modify a table header name
@click.command()
@click.argument('filename', type=click.Path())
@click.argument('old_header_name')
@click.argument('new_header_name')
def modify_table_header(filename, old_header_name, new_header_name):
    """Modify a table header name.

    Args:
        filename (str): Name of the SQLite database file.
        old_header_name (str): Current name of the table header.
        new_header_name (str): New name for the table header.
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
            print(f"Table header name '{old_header_name}' changed to '{new_header_name}' successfully.")
        else:
            print(f"Table header '{old_header_name}' does not exist.")
    except sqlite3.Error as e:
        print(f"Error modifying table header name: {str(e)}")
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
def lock_database(file_path, password, confirm_password):
    """Lock the SQLite database with encryption.

    Args:
        file_path (str): Name of the SQLite database file.
        password (str): Encryption password.
        confirm_password (str): Confirmation of encryption password.
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

        print(f"File '{file_path}' is now locked and cannot be read or modified.")
    except Exception as e:
        print(f"Error encrypting file: {str(e)}")

# Function to decrypt database
@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('password', type=str)
def unlock_database(file_path, password):
    """Unlock the SQLite database with decryption.

    Args:
        file_path (str): Name of the SQLite database file.
        password (str): Decryption password.
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

        print(f"File '{file_path}' is unlocked and can now be read and modified.")
    except Exception as e:
        print(f"Error decrypting file: {str(e)}")

@click.group()
def cli():
    """Command-line interface for managing an SQLite database.
    """
    pass

# Add commands to the click CLI
cli.add_command(make_database, name='make-db')
cli.add_command(insert_table_header, name='insert-th')
cli.add_command(add_table_data, name='add-td')
cli.add_command(search_data, name='search-td')
cli.add_command(remove_data, name='remove-td')
cli.add_command(modify_data, name='modify-td')
cli.add_command(remove_table_header, name='remove-th')
cli.add_command(modify_table_header, name='modify-th')
cli.add_command(lock_database, name='lock-db')
cli.add_command(unlock_database, name='unlock-db')

# Run the CLI
if __name__ == '__main__':
    cli()
