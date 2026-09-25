# Personal Expense Tracker (CLI)

A terminal application for expense management and the creation of expense-related statistics and reports.

## Features

- JSON persistence in local storage
- Expense filtering
- Expense montly/yearly reports
- Input validation
- Custom exceptions
- Unit tests

## Project structure
```
Personal_Expense_Tracker/
├── data/           -> data persistence
├── enums/          -> enumerations
├── exception/      -> custom exceptions
├── logs/           -> application logs
├── src/            -> application
├── tests/          -> tests and static test data
├── README.md
├── LICENSE
├── requirements.txt
└── .gitignore
```

## Requirements
**Runtime**: Python 3.7 or later

**Development**: pytest 9.1.1

## Installation

1. Clone the project on your PC or download it

2. Create and activate a virtual environment:

   - Linux / macOS:

   ```bash
    python -m venv .venv
    source .venv/bin/activate
   ```

   - Windows (PS):

   ```powershell
   python -m venv .venv
   .\venv\Scripts\Activate.ps1
   ```

   - Windows (cmd):

   ```cmd
   python -m venv .venv
   venv\Scripts\Activate.bat
   ```
3. Install the project dependencies in your virtual enviroment:
    ```
    pip install -r requirements.txt
    ```

## Usage
Run the application from the project root using:
```
python -m src.main
```
Make sure the virtual environment is activated before running the application.

A terminal window will appear with a menu containing the following options:

1. Expense Management
2. Expense Statistics
3. Expense Report
4. Exit


The first option lets you manage your expenses: add, search for, edit, or delete expenses

The second option lets you see the total, average, maximum, minimum and balance of all or filtered expenses

The third option allows you to choose whether to view the report for a specific year or a specific month

## Running tests

To run all the tests (after installing the project dependencies) use the command:
```
python -m pytest
```

or if you want a specific test file use e.g.:
```
python -m pytest tests/test_storage.py
```
## Data persistence

The application uses a JSON file to persist expense data.

If the data file does not exist when the application is first executed, the application handles the missing file without loading any expenses.

## Future improvements

- Improve the application menu.

## License

MIT License