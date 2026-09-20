# Program starter

## Standard Library
import logging

## Local project imports
from src.menu import main_menu, handle_corrupted_file
from src.storage import load_expenses
from src.filters import set_filter_list
from exception.exceptions import StorageDataCorruptedError

logging.basicConfig(
	filename="logs/expense_tracker.log",
	filemode="a",
	encoding="UTF-8",
	format="{levelname}.{name} - {asctime} -> {message}",
	datefmt="%Y/%m/%d %H:%M:%S",
	style="{",
	level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
	logger.info("Program started")
	continue_execution = True
	try:
		load_expenses()
	except StorageDataCorruptedError:
		continue_execution = handle_corrupted_file()

	if continue_execution:
		set_filter_list()
		main_menu()
	else:
		logger.info("The program terminated due to a backup error or by user choice") 

	logger.info("Program finished")


if __name__ == "__main__":
	main()