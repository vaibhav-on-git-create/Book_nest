import json

def append_json(file_path: str, data_dict: dict):
    try:
        with open(file_path, "r") as file_1:
            previous_data = json.load(file_1)

    except json.JSONDecodeError:
        previous_data = {}

    previous_data.update(data_dict)

    with open(file_path, "w") as file_2:
        json.dump(previous_data, file_2, indent=4)


def edit_json_key(file_path : str , key : str , new_value : str):
    try:

        with open(file_path , "r") as file_1:
            data = json.load(file_1)
            dict_keys = data.keys()

            if key in dict_keys:

                data.update({key:new_value})
                file_1.close()

                with open(file_path , "w") as file_2:
                    json.dump(data , file_2 , indent=4)
                    print(f"updated the file : [{file_path}] -- updated : [{key}] to new value : [{new_value}]")

            else:
                print(f"The key : [{key}] was not found in file [{file_path}]")

    except Exception as e:
        print(f"An error occured : [{e}]")


# add_book.name = "Physics"
# add_book.author = "hc verma"
# add_book.price = 300
# add_book.times_issued = 0
# add_book.avl_copies = 100
# add_book.section = "class 11 and 12"
# pay_load = add_book().generate_payload()


# edit_json_key(file_path =r"D:\My_projects\Book_nest\Books\Maths_class_12.json" , key = "author" , new_value= "RD sharma")

def read_json(file_path : str , key = None):
    with open(file_path , "r") as file:
        data = json.load(file)
        if key is None :
            return data
        else:
            keys = data.keys()
            if key in keys:
                return data[key]
            else:
                print(f"the key : [{key}] was not foud in file : [{file_path}]")
                return None
            

