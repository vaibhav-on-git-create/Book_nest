import console_tools

def main_console():
    print(console_tools.frames.welcome_message())
    print(console_tools.frames.display_options())
    print("Type 'exit' to quit the console")
    user_choice = input("Enter your choice (number): ")

    if user_choice == "1":
        console_tools.add_book_record()
    if user_choice == "2":
        console_tools.edit_book_record()
    if user_choice == "3":
        console_tools.check_book_status()
    if user_choice == "4":
        console_tools.remove_book()
    if user_choice == "5":
        console_tools.find_books()
    if user_choice == "6":
        console_tools.find_issues()
    
    if user_choice == "exit":
        exit()
        
main_console()