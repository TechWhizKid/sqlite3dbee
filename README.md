# SQLite Database Management Command-Line Tool

A versatile command-line tool built in Python for managing SQLite databases effortlessly. This tool offers a range of commands to facilitate database creation, table manipulation, data addition, search, removal, and modification.

## Features

- **Database Creation:** Easily create new SQLite database files with a simple command.
- **Table Management:** Create tables with customizable headers, modify header names, and even remove entire tables.
- **Data Manipulation:** Add, search, modify, and remove rows of data within tables.
- **User-Friendly Interface:** Utilizes the Click library to ensure a smooth and user-friendly command-line experience.
- **Flexibility:** The tool provides multiple commands to perform different database operations.

## Prerequisites

- Python (3.6 or higher) installed on your system.
- The Click and tabulate library. Install it using:

```
pip install click tabulate
```

## Installation

1. Clone this repository:

```
git clone https://github.com/TechWhizKid/sqlite3dbee.git
```

2. Navigate to the cloned directory:

```
cd sqlite3dbee-main
```

3. Run the tool:

```
python sqlite3dbee.py [command]
```

## Usage

Below are the available commands and their usage:

```batch
Usage: sqlite3dbee.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add_td     Add a new row of data to the table.
  insert_th  Create a table with specified headers.
  makedb     Create a new SQLite database file.
  modify_td  Modify rows in the table based on criteria.
  modify_th  Modify a table header name.
  remove_td  Remove rows from the table based on criteria.
  remove_th  Remove a table header and its data.
  search     Search for rows in the table based on criteria.
```

- Create a new database:

```py
sqlite3dbee.py makedb sql3_database.db
```

- Insert new table headers:

```py
sqlite3dbee.py insert_th sql3_database.db No Title Username Password
```

- Add data to the table:

```py
sqlite3dbee.py add_td sql3_database.db "No:1" "Title:Dummy" "Username:John Doe" "Password:StrongDummyPasswd"
```

- Search for data:

```py
sqlite3dbee.py search sql3_database.db
sqlite3dbee.py search sql3_database.db "Username = 'John Doe'"
```

- Remove data:

```py
sqlite3dbee.py remove_td sql3_database.db "Username = 'John Doe'"
```

- Modify data:

```py
sqlite3dbee.py modify_td sql3_database.db "Username = 'John Doe'" "Password='NewVeryStrongPasswd'"
```

- Remove a table header and its data:

```py
sqlite3dbee.py remove_th sql3_database.db Title
```

- Modify a table header name:

```py
sqlite3dbee.py modify_th sql3_database.db Username new_users
```

## License

This project is licensed under the [MIT License](https://github.com/TechWhizKid/sqlite3dbee/blob/main/LICENSE)

---

Empower your SQLite database management with this intuitive command-line tool. Whether you're a developer or a data enthusiast, this tool simplifies your interactions with SQLite databases.
