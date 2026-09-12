import menu, storage

if __name__ == "__main__":
	storage.load_expenses()
	menu.expense_menu()