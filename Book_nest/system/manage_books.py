import generate_serial
import datetime
from datetime import datetime, timedelta
import manage_dir
import json_tools


def generate_available_serial(num: int):
    return [generate_serial.generate_serial() for _ in range(num)]


def date_after_n_days(start_date_str, n):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    new_date = start_date + timedelta(days=n)
    return new_date.strftime("%Y-%m-%d")


class add_book:
    name = ""
    author = ""
    price = 0
    times_issued = 0
    avl_copies = 0
    section = ""

    def generate_payload(self):
        avl_serial = generate_available_serial(num=self.avl_copies)
        payload = {
            "name": self.name,
            "author": self.author,
            "price": self.price,
            "times_issued": self.times_issued,
            "available_copies": self.avl_copies,
            "available_serials": avl_serial,
            "issued_serials": []
        }
        return payload


def find_books(serial: str = "0", path=False):
    target = "json"
    books_names = [i.replace(".json", "") for i in manage_dir.list_dir(folder_path="../Book_nest/Books", target=target, path=False)]
    books_path = manage_dir.list_dir(folder_path="../Book_nest/Books", target=target, path=True)
    serials = [json_tools.read_json(file_path=file, key="available_serials") for file in books_path]

    index = None
    for iter_serial in serials:
        if serial in iter_serial:
            index = serials.index(iter_serial)
            break

    if index is not None:
        if path:
            return books_path[index]
        else:
            return books_names[index]
    return None

def find_issues(issue_id: str = "0", path=False):
    target = "json"
    issues_names = [i.replace(".json", "") for i in manage_dir.list_dir(folder_path="../Book_nest/Issues", target=target, path=False)]
    issues_path = manage_dir.list_dir(folder_path="../Book_nest/Issues", target=target, path=True)
    issue_ids = [json_tools.read_json(file_path=file, key="issue_id") for file in issues_path]

    index = None
    for iter_id in issue_ids:
        if issue_id == iter_id:
            index = issue_ids.index(iter_id)
            break

    if index is not None:
        if path:
            return issues_path[index]
        else:
            return issues_names[index]
    return None

def generate_book_list(serial_list: list):
    # mentioning the book name and how many copies of it were issued
    book_list = []
    for serial in serial_list:
        book_name = find_books(serial=serial)
        if book_name is not None:
            found = False
            for item in book_list:
                if item[0] == book_name:
                    item[1] += 1
                    found = True
                    break
            if not found:
                book_list.append([book_name, 1])

    return book_list
    
    

def issue_books(serial_list: list):
    return [[serial, find_books(serial=serial)] for serial in serial_list]

#print(issue_books(serial_list=["101", "102", "201", "202", "101"]))


def list_all_issued_books():
    all_issued_serials = []
    issues_path = manage_dir.list_dir(folder_path="../Book_nest/Issues", target="json", path=True)
    for issue_file in issues_path:
        issued_serials = json_tools.read_json(file_path=issue_file, key="book_serials")
        for serial_pair in issued_serials:
            all_issued_serials.append(serial_pair[0])
    return all_issued_serials

def remove_issued_serials(serial :str):
    book_name = find_books(serial=serial)
    if book_name is not None:
        book_path = manage_dir.list_dir(folder_path="../Book_nest/Books", target=book_name, path=True)[0]
        book_data = json_tools.read_json(file_path=book_path)
        issued_serial = book_data["issued_serials"]
        if serial in issued_serial:
            issued_serial.remove(serial)
            json_tools.edit_json_key(file_path=book_path, key="issued_serials", new_value=issued_serial)

        else:
            print(f"The serial : [{serial}] was ]not issued according to the book data")

    if book_name is None:
        print(f"The serial : [{serial}] was not found in any book")
            

    


class issue_book:

    name = "name"
    grade = "grade"
    section = "section"
    copies_issued = [1]
    serial_numbers = ["0"]
    book_names = issue_books(serial_list=serial_numbers)
    issue_days = 7
    issue_date = datetime.now().date()
    return_date = date_after_n_days(str(issue_date), issue_days)
    
    issue_id = generate_serial.generate_issue_id(name=name, grade=grade, sec=section)


    def generate_payload(self):
        payload = {
            "name": self.name,
            "grade": self.grade,
            "section": self.section,
            "book_name": self.book_names,
            "copies_issued": self.copies_issued,
            "book_serials": issue_books(serial_list=self.serial_numbers),
            "books_count": generate_book_list(serial_list=self.serial_numbers),
            "issue_days": self.issue_days,
            "issue_date": self.issue_date.strftime("%Y-%m-%d"),
            "return_date": self.return_date,
            "issue_id": self.issue_id.replace(" ", "")

        }
        return payload



    
    

    
