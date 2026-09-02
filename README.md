# Personal Expense Tracker (CLI)

A terminal application for managing income, expenses, categories, and statistics, with data saved to a file.


## Installation

1. Clone the project on your pc or download it

2. Create and activate a virtual envirioment:

   - Linux / macOS:

   ```bash
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   ```

   - Windows (PS):

   ```powershell
   python3.exe -m venv .venv
   .\venv\Scripts\Activate.ps1
   ```

   - Windows (cmd):

   ```cmd
   python3.exe -m venv .venv
   venv\Scripts\Activate.bat
   ```
4. Add the projects requriments in your virtual envirioment:
    ```
    pip install -r requirements.txt
    ```


## How it work

Run the main.py (REMEBER TO ACTIVATE THE VIRTUAL ENVIRIOMENT) or the PersonaExpenseTracker.exe (end of project)
and a terminal window will appear with a menu asking you to choose one of the following options:

1. Insert income
2. Insert expenses
3. Search expenses
4. Show expenses statistics
5. Show expenses report

The first three options are straightforward: just enter your information and submit;

In **4** Search expenses, you can filter expenses by: data, tag or amount;

In **5** Show expenses statistics, you see the total, average, maximum, minimum and balance;

In **6** Show expenses report, you can chose to see the annual or a particular mounth report;
