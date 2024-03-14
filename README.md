# SQLite Database Management Command-Line Tool

Effortlessly manage SQLite databases with this versatile command-line tool built in Python. Simplify tasks such as creating databases, managing tables, manipulating data, and encrypting/decrypting sql files, all through a user-friendly command line interface.

## Features

- **Database Creation:** Easily create new SQLite database files with a simple command.
- **Table Management:** Create tables with customizable headers, modify header names, and even remove entire tables.
- **Data Manipulation:** Add, search, modify, and remove rows of data within tables.
- **Database Encryption** Encrypt and decrypt SQL database files with password protection.
- **User-Friendly Interface:** Utilizes the Click library to ensure a smooth and user-friendly command-line experience.
- **Flexibility:** The tool provides multiple commands to perform different database operations.

## Prerequisites

- Python (3.6 or higher) installed on your system.
- The click, tabulate and cryptography library. Install it using:

```batch
pip install click tabulate cryptography
```

## Installation

1. Clone this repository:

```batch
git clone https://github.com/TechWhizKid/sqlite3dbee.git
```

2. Navigate to the cloned directory:

```batch
cd sqlite3dbee-main
```

3. Run the tool:

```batch
python sqlite3dbee.py [OPTIONS] [COMMAND] <filename> [ARGS]
```

## Usage

Below are the available commands and their usage examples:

```bash
Usage: sqlite3dbee.py [OPTIONS] [COMMAND] <filename> [ARGS]

  Command-line interface for managing an SQLite database.

Options:
  --help Show help message and exit.

Commands:
  mkdb  Create a new SQLite database file.
  adth  Create a table with specified headers.
  adtd  Add a new row of data to the table.
  mdth  Modify a table header name.
  mdtd  Modify rows in the table based on criteria.
  sctr  Search for rows in the table based on criteria.
  rmtr  Remove rows from the table based on criteria.
  rmtc  Remove a column from a table in the database.
  lkdb  Lock the SQLite database with encryption.
  ukdb  Unlock the SQLite database with decryption.
  help  Show this message and exit.
  xmpl  Shows a help message with usage example.
```

#### Examples:

- Create a new SQL database file:

```bash
sqlite3dbee.py mkdb database.sql
```

- Insert new table headers:

```bash
sqlite3dbee.py adth database.sql "Name" "Age" "UserName" "UserID"
```

- Add data to the table:

```bash
sqlite3dbee.py adtd database.sql "Name":"Robby Russel" "Age":"25" "UserName":"robby_fr" "UserID":"1029384756"
```

- Search for data in table:

```bash
sqlite3dbee.py sctr database.sql
sqlite3dbee.py sctr database.sql "Age = '26'"
```

- Remove a row of data from the table:

```bash
sqlite3dbee.py rmtr database.sql "UserName = 'robby_fr'"
```

- Modify table data:

```bash
sqlite3dbee.py mdtd database.sql "Age = '25'" "Age = '26'"
```

- Remove a table column and its data:

```bash
sqlite3dbee.py rmtc database.sql "UserName"
```

- Modify a table header name:

```bash
sqlite3dbee.py mdth database.sql "Name" "RealName"
```

- Lock the database file

```bash
sqlite3dbee.py lkdb database.sql "123456" "123456"
```

- Unlock the database file

```bash
sqlite3dbee.py ukdb database.sql "123456"
```

## License

This project is licensed under the [MIT License](https://github.com/TechWhizKid/sqlite3dbee/blob/main/LICENSE)

---

Empower your SQLite database management with this intuitive command-line tool. Whether you're a developer or a data enthusiast, this tool simplifies your interactions with SQLite databases.
