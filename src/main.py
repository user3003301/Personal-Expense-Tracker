from src import menu, storage, filters
from exception.exceptions import StorageDataCorruptedError

if __name__ == "__main__":
	operation = True
	try:
		storage.load_expenses()
	except StorageDataCorruptedError:
		operation = menu.handle_corrupted_file()

	if operation:
		filters.set_filter_list()
		menu.main_menu()
	else: 
		exit()