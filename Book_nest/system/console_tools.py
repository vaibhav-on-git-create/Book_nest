import manage_books as mb
import json_tools
import json
import manage_dir
import generate_serial
import os

books_database = "../Book_nest/Books"
issues_data_base = "../Book_nest/Issues"

def safe_intput(statement: str, dt=str):
    while True:
        try:
            return dt(input(statement))
        except ValueError:
            print(f"Invalid input. Please enter a valid {dt.__name__}.")

class frames:
    print(">>> System")

    def welcome_message():
        welcome = f"""
        _________________________________________________________________________________________
        |                                                                                         |
        |           Welcome to Book Nest - Your Ultimate Library Management System!               |
        |                                                                                         |
        |   Manage your books, track issues, and keep your library organized with ease.          |
        |                                                                                         |
        |_________________________________________________________________________________________|
        """
        return welcome

    def display_options():
        options = f"""
        ______________________[your options are]___________________________________________________
        |       1. [add book] | 2. [edit book] | 3. [check book status] | 4. [remove book]         |
        |                                                                                         |
        |       5. [find book by serial] | 6. [check issued book] | 7. [get issued books records] |
        |                                                                                         |
        |       8. [send reminder to borrower] | 9. [get borrower detail] | 10. [remove borrower] |
        |                                                                                         |
        |       You requested to type the option number of the operation you want to perform      |
        |_________________________________________________________________________________________|
        """
        return options

    @staticmethod
    def display_student(name, grade, section):
        student = f"|NAME : {str(name)} |GRADE : {str(grade)} |SECTION : {str(section)} |"
        length = len(student)
        return f"{'_'*length}\n{student}\n{'-'*length}"

    @staticmethod
    def display_books(serial, book, Author):
        book_display = f"|SERIAL : {serial} |BOOK NAME : {book} |AUTHOR : {Author}  |"
        length = len(book_display)
        return f"{'_'*length}\n{book_display}\n{'-'*length}"

    @staticmethod
    def display_book_record(book_name: str, Author: str, book_price: str, num_copies: int):
        book_display = (f"|BOOK NAME : {book_name} |AUTHOR : {Author} |BOOK PRICE : {book_price} |"
                        f"Number of copies: {num_copies} |")
        length = len(book_display)
        return f"{'_'*length}\n{book_display}\n{'-'*length}"

    @staticmethod
    def display_all_records():
        target = "json"
        file_names = [i.replace(f".{target}", "") for i in manage_dir.list_dir(folder_path=books_database, target=target, path=False)]
        file_paths = manage_dir.list_dir(folder_path=books_database, target=target, path=True)
        if not file_names or not file_paths:
            print("No book records found.")
            return
        display_details = []
        for i in range(len(file_names)):
            append_text = f"| SR : {i+1} |BOOK NAME : {file_names[i]} |FILE LOCATION : {file_paths[i]} |"
            line_1 = '_'*len(append_text)
            line_2 = '-'*len(append_text)
            display_details.extend([line_1, append_text, line_2])
        for j in display_details:
            print(j)

    @staticmethod
    def display_book_data(name, author, price, available_copies):
        book_data = (f"|1. BOOK NAME : {name} |2. AUTHOR : {author} |3. PRICE : {price} |"
                     f"4. AVAILABLE COPIES : {available_copies} |")
        length = len(book_data)
        return f"{'_'*length}\n{book_data}\n{'-'*length}"

    @staticmethod
    def display_issue_record(name, grade, section, book_names, copies_issued, issue_date, return_date, issue_id):
        issue_data = (f"|NAME : {name} |GRADE : {grade} |SECTION : {section} |BOOKS ISSUED : {book_names} |"
                      f"COPIES ISSUED : {copies_issued} |ISSUE DATE : {issue_date} |RETURN DATE : {return_date} |"
                      f"ISSUE ID : {issue_id} |")
        length = len(issue_data)
        return f"{'_'*length}\n{issue_data}\n{'-'*length}"

    @staticmethod
    def display_book_details(serial_book_list: list):
        serial, book = serial_book_list[0], serial_book_list[1]
        book_display = f"|SERIAL : {serial} |BOOK NAME : {book} |"
        length = len(book_display)
        return f"{'_'*length}\n{book_display}\n{'-'*length}"

    @staticmethod
    def display_book_counts(books_count_list: list):
        book_name, count = books_count_list[0], books_count_list[1]
        book_display = f"|BOOK NAME : {book_name} |COUNT : {count} |"
        length = len(book_display)
        return f"{'_'*length}\n{book_display}\n{'-'*length}"

def add_book_record():
    book_name = input("Enter the Book name : ").strip()
    if not book_name:
        print("Book name is required. Aborting operation.")
        return
    file_path = os.path.join(books_database, f"{book_name}.json")
    if not os.path.exists(file_path):
        author = input("Enter the Author name : ").strip()
        book_price = input("Enter the Book price : ").strip()
        try:
            num_copies = int(input("Enter the number of copies : ").strip())
        except ValueError:
            print("Invalid number of copies. Aborting operation.")
            return

        print(frames.display_book_record(book_name=book_name, Author=author, book_price=book_price, num_copies=num_copies))
        user_choice = input("Is the above information correct ? (y/n) : ").strip().lower()

        if user_choice == "y":
            if not os.path.exists(books_database):
                os.makedirs(books_database)
            mb.add_book.name = book_name
            mb.add_book.author = author
            mb.add_book.price = book_price
            mb.add_book.available_copies = num_copies
            payload = mb.add_book().generate_payload()
            json_tools.append_json(file_path=file_path, data_dict=payload)
            print("Book record added successfully.")
        else:
            print("Aborting operation ...")
    else:
        print(f"The book : [{book_name}] already exists")

def edit_book():
    frames.display_all_records()
    all_books_path = manage_dir.list_dir(folder_path=books_database, target="json", path=True)
    if not all_books_path:
        print("No books available to edit.")
        return
    print("You are requested to choose any one sr number for further operation :)")
    sr = safe_intput(statement="enter your choice : ", dt=int)
    if sr < 1 or sr > len(all_books_path):
        print("Invalid selection. Aborting operation.")
        return
    file_path = all_books_path[sr - 1]
    book_data = json_tools.read_json(file_path=file_path)

    frames.display_book_data(name=book_data.get("name", ""), author=book_data.get("author", ""), price=book_data.get("price", ""),
                            available_copies=book_data.get("available_copies", 0))
    print("You are requested to choose any one option number for further operation :)")
    option = safe_intput(statement="enter your choice : ", dt=int)

    if option == 1:
        new_name = input("Enter the new book name : ").strip()
        json_tools.edit_json_key(file_path=file_path, key="name", new_value=new_name)
    elif option == 2:
        new_author = input("Enter the new author name : ").strip()
        json_tools.edit_json_key(file_path=file_path, key="author", new_value=new_author)
    elif option == 3:
        new_price = input("Enter the new book price : ").strip()
        json_tools.edit_json_key(file_path=file_path, key="price", new_value=new_price)
    elif option == 4:
        new_copies = safe_intput(statement="Enter the new available copies : ", dt=int)
        previous_serials = book_data.get("available_serials", [])
        issued_serials = book_data.get("issued_serials", [])
        previous_copies = len(previous_serials)

        if new_copies > previous_copies:
            difference = new_copies - previous_copies
            new_serials = mb.generate_available_serial(num=difference)
            updated_serials = previous_serials + new_serials
            json_tools.edit_json_key(file_path=file_path, key="available_serials", new_value=updated_serials)
        elif new_copies < previous_copies:
            difference = previous_copies - new_copies
            removable_serials = [serial for serial in previous_serials if serial not in issued_serials]

            if difference > len(removable_serials):
                print("Cannot remove this many copies because too many are issued.")
                print("Aborting operation ...")
                return

            serials_to_remove = removable_serials[:difference]
            updated_serials = [serial for serial in previous_serials if serial not in serials_to_remove]
            json_tools.edit_json_key(file_path=file_path, key="available_serials", new_value=updated_serials)

        json_tools.edit_json_key(file_path=file_path, key="available_copies", new_value=new_copies)
    else:
        print("Invalid option selected. Aborting operation ...")

def remove_book():
    frames.display_all_records()
    all_books_path = manage_dir.list_dir(folder_path=books_database, target="json", path=True)
    if not all_books_path:
        print("No books available to remove.")
        return
    print("You are requested to choose any one sr number for further operation :)")
    sr = safe_intput(statement="enter your choice : ", dt=int)
    if sr < 1 or sr > len(all_books_path):
        print("Invalid selection. Aborting operation.")
        return
    file_path = all_books_path[sr - 1]
    book_data = json_tools.read_json(file_path=file_path)

    issued_serials = book_data.get("issued_serials", [])

    if len(issued_serials) > 0:
        print("Cannot remove this book because some copies are currently issued.")
        print("Aborting operation ...")
        return

    os.remove(file_path)
    print(f"Book record at [{file_path}] has been successfully removed.")

def check_book_status():
    frames.display_all_records()
    all_books_path = manage_dir.list_dir(folder_path=books_database, target="json", path=True)
    if not all_books_path:
        print("No books available.")
        return
    print("You are requested to choose any one sr number for further operation :)")
    sr = safe_intput(statement="enter your choice : ", dt=int)
    if sr < 1 or sr > len(all_books_path):
        print("Invalid selection. Aborting operation.")
        return
    file_path = all_books_path[sr - 1]
    book_data_json = json_tools.read_json(file_path=file_path)
    issued_books = book_data_json.get("issued_serials", [])
    if not issued_books:
        print("No issued copies for this book.")
        return
    for i in issued_books:
        issue_record_file = os.path.join(issues_data_base, f"{i}.json")
        if os.path.exists(issue_record_file):
            borrower_detail = json_tools.read_json(file_path=issue_record_file)
            print(frames.display_student(name=borrower_detail.get("name", ""),
                                         grade=borrower_detail.get("grade", ""),
                                         section=borrower_detail.get("section", "")))
        else:
            print(f"Borrower record for issued serial {i} not found.")

def find_books():
    serial = safe_intput(statement="Enter the serial number to search for: ", dt=str)
    user = input("Do you want the file path as well? (y/n): ").strip()
    path = True if user.lower() == "y" else False
    all_books_names = manage_dir.list_dir(folder_path=books_database, target="json", path=False)
    all_books_path = manage_dir.list_dir(folder_path=books_database, target="json", path=True)
    book_name = mb.find_books(serial=serial, path=path)

    if book_name is not None:
        if not path:
            book_path_index = all_books_names.index(f"{book_name}.json")
            book_path = all_books_path[book_path_index]
            book_data = json_tools.read_json(file_path=book_path)
            print(frames.display_book_data(name=book_data.get("name", ""),
                                          author=book_data.get("author", ""),
                                          price=book_data.get("price", ""),
                                          available_copies=book_data.get("available_copies", 0)))
        else:
            book_data = json_tools.read_json(file_path=book_name)
            print(frames.display_book_data(name=book_data.get("name", ""),
                                          author=book_data.get("author", ""),
                                          price=book_data.get("price", ""),
                                          available_copies=book_data.get("available_copies", 0)))
            print(f"File path: {book_name}")
    else:
        print(f"No book found with serial number: {serial}")

def issue_books():
    name = safe_intput(statement="Enter the borrower's name: ", dt=str).strip().lower()
    grade = safe_intput(statement="Enter the borrower's grade: ", dt=str).strip().lower()
    section = safe_intput(statement="Enter the borrower's section: ", dt=str).strip().lower()
    num_copies = safe_intput(statement="Enter the number of copies to issue: ", dt=int)
    print("Enter the serial numbers of the books to issue separated by commas:")
    serials_input = input(">>>").strip()

    all_issued_serials = mb.list_all_issued_books()
    all_borrower_list = manage_dir.list_dir(folder_path=issues_data_base, target="json", path=False)

    if num_copies <= 0:
        print("Number of copies must be greater than zero. Aborting operation ...")
        return
    if num_copies > 10:
        print("Cannot issue more than 10 copies at once. Aborting operation ...")
        return

    if num_copies == 1:
        serials_to_issue = [serials_input]
        if serials_to_issue[0] in all_issued_serials:
            print(f"The serial number [{serials_to_issue[0]}] is already issued. Aborting operation ...")
            return
    else:
        serials_to_issue = [i.strip() for i in serials_input.split(",") if i.strip()]
        for serial in serials_to_issue:
            if serial in all_issued_serials:
                print(f"The serial number [{serial}] is already issued. Aborting operation ...")
                return

    if len(serials_to_issue) != num_copies:
        print(f"Warning: Number of serials entered ({len(serials_to_issue)}) does not match number of copies requested ({num_copies}).")
        return

    book_names = mb.issue_books(serial_list=serials_to_issue)
    num_copies_issued = len(book_names)

    file_name = f"{name}_{grade}_{section}"

    if file_name in all_borrower_list:
        print(f"The borrower [{name}] in grade [{grade}] section [{section}] already has an active issue record.")
        print("Aborting operation ...")
        return

    mb.issue_book.name = name
    mb.issue_book.grade = grade
    mb.issue_book.section = section
    mb.issue_book.copies_issued = num_copies_issued
    mb.issue_book.serial_numbers = serials_to_issue
    book_array = [mb.issue_books]
    mb.issue_book.book_names = [books[1] for books in mb.issue_books(serial_list=serials_to_issue)]
    payload = mb.issue_book().generate_payload()

    manage_dir.create_dir(name=file_name, root_dir="issue", ext="json")

    issue_file_paths = manage_dir.list_dir(folder_path=issues_data_base, target=file_name, path=True)
    if issue_file_paths:
        issue_file_path = issue_file_paths[0]
    else:
        issue_file_path = os.path.join(issues_data_base, f"{file_name}.json")
        with open(issue_file_path, "w") as file:
            json.dump({}, file)

    json_tools.append_json(file_path=issue_file_path, data_dict=payload)
    print(f"Issued {num_copies_issued} copies successfully to {name}.")

def find_issues():
    issue_id = safe_intput(statement="Enter the issue Serial to search for: ", dt=str).strip()
    user = input("Do you want the file path as well? (y/n): ").strip()
    path = True if user.lower() == "y" else False
    all_issues_names = manage_dir.list_dir(folder_path=issues_data_base, target="json", path=False)
    all_issues_path = manage_dir.list_dir(folder_path=issues_data_base, target="json", path=True)
    issue_name = mb.find_issues(issue_id=issue_id, path=path)

    if issue_name is not None:
        if not path:
            issue_path_index = all_issues_names.index(f"{issue_name}.json")
            issue_path = all_issues_path[issue_path_index]

            issue_data = json_tools.read_json(file_path=issue_path)
            print(frames.display_student(name=issue_data.get("name", ""), grade=issue_data.get("grade", ""), section=issue_data.get("section", "")))

            books_count_list = issue_data.get("books_count", [])
            for book_count in books_count_list:
                print(frames.display_book_counts(books_count_list=book_count))

            book_serials_list = issue_data.get("book_serials", [])
            for serial_book in book_serials_list:
                print(frames.display_book_details(serial_book_list=serial_book))
        else:
            issue_data = json_tools.read_json(file_path=issue_name)
            print(frames.display_student(name=issue_data.get("name", ""), grade=issue_data.get("grade", ""), section=issue_data.get("section", "")))
            print(f"File path: {issue_name}")
    else:
        print(f"No issue found with issue ID: {issue_id}")
