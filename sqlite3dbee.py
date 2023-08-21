import sqlite3
import click
import tabulate

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

        print("Row added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding row: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to search for data based on criteria
@click.command(name='search')
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

        print("Rows removed successfully.")
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
@click.command(name='remove_th')
@click.argument('filename', type=click.Path())
@click.argument('header_name')
def remove_table_header(filename, header_name):
    """Remove a table header and its data.

    Args:
        filename (str): Name of the SQLite database file.
        header_name (str): Name of the table header to be removed.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(filename)
        cursor = connection.cursor()

        # Construct the DROP TABLE query
        drop_table_query = f"DROP TABLE IF EXISTS {header_name}"
        cursor.execute(drop_table_query)
        connection.commit()

        print(f"Table header '{header_name}' and its data removed successfully.")
    except sqlite3.Error as e:
        print(f"Error removing table header: {str(e)}")
    finally:
        if connection:
            connection.close()

# Function to modify a table header name
@click.command(name='modify_th')
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

@click.group()
def cli():
    """Command-line interface for managing an SQLite database.
    """
    pass

cli.add_command(make_database, name='makedb')
cli.add_command(insert_table_header, name='insert_th')
cli.add_command(add_table_data, name='add_td')
cli.add_command(search_data, name='search')
cli.add_command(remove_data, name='remove_td')
cli.add_command(modify_data, name='modify_td')
cli.add_command(remove_table_header, name='remove_th')
cli.add_command(modify_table_header, name='modify_th')

if __name__ == '__main__':
    cli()
