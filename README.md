# SQLite Database Management Command-Line Tool

Effortlessly manage SQLite databases with this versatile command-line tool built in Python. Simplify tasks such as creating databases, managing tables, manipulating data, and encrypting/decrypting sql files, all through a user-friendly interface.

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
python sqlite3dbee.py [OPTIONS] COMMAND [ARGS]...
```

## Usage

Below are the available commands and their usage examples:

```bash
Usage: sqlite3dbee.py [OPTIONS] COMMAND [ARGS]...

  Command-line interface for managing an SQLite database.

Options:
  --help  Show this message and exit.

Commands:
  add-td     Add a new row of data to the table.
  insert-th  Create a table with specified headers.
  lock-db    Lock the SQLite database with encryption.
  make-db    Create a new SQLite database file.
  modify-td  Modify rows in the table based on criteria.
  modify-th  Modify a table header name.
  remove-td  Remove rows from the table based on criteria.
  remove-th  Remove a table header and its data.
  search-td  Search for rows in the table based on criteria.
  unlock-db  Unlock the SQLite database with decryption.
```

#### Examples:

- Create a new SQL database file:

```bash
sqlite3dbee.py make-db database.sql
```

- Insert new table headers:

```bash
sqlite3dbee.py insert-th database.sql "No" "Title" "Username" "Password"
```

- Add data to the table:

```bash
sqlite3dbee.py add-td database.sql "No:1" "Title:GitHub" "Username:John Doe" "Password:StrongDummyPassword"
```

- Search for data in table:

```bash
sqlite3dbee.py search-td database.sql
sqlite3dbee.py search-td database.sql "Username = 'John Doe'"
```

- Remove data from the table:

```bash
sqlite3dbee.py remove-td database.sql "Username = 'John Doe'"
```

- Modify table data:

```bash
sqlite3dbee.py modify-td database.sql "Username = 'John Doe'" "Password='VeryStrongNewPassword'"
```

- Remove a table header and its data:

```bash
sqlite3dbee.py remove-th database.sql "Title"
```

- Modify a table header name:

```bash
sqlite3dbee.py modify-th database.sql Username new_users
```

- Lock the database file

```bash
sqlite3dbee.py lock-db database.sql <password> <conform-password>
```

- Unlock the database file

```bash
sqlite3dbee.py unlock-db database.sql <password>
```

## License

This project is licensed under the [MIT License](https://github.com/TechWhizKid/sqlite3dbee/blob/main/LICENSE)

---

Empower your SQLite database management with this intuitive command-line tool. Whether you're a developer or a data enthusiast, this tool simplifies your interactions with SQLite databases.
