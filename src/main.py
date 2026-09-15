import menu, storage, filters

if __name__ == "__main__":
	storage.load_expenses()
	filters.set_filter_list()
	menu.main_menu()