import os


def create_dir(name: str , root_dir: str = "book", ext: str = "json"):
    root_path = None

    if root_dir == "book":
        root_path = "../Book_nest/Books"
    elif root_dir == "issue":
        root_path = "../Book_nest/Issues"

    file_name = f"{name}.{ext}"
    file_path = os.path.join(root_path, file_name)
    
  
    os.makedirs(root_path, exist_ok=True)

    
    if os.path.exists(file_path):
        print(f"File with name: [{file_name}] already exists at [{file_path}]")
    else:

        with open(file_path, 'w') as file:
            pass
        print(f"Creation successful at [{file_path}]")


create_dir(name="English_class_12", ext="json", root_dir="book")

def list_dir(folder_path : str , target = None , path = True):
    if target == None:
            
        if os.path.exists(path = folder_path):
            file_names = os.listdir(path = folder_path)

            if path:
                return [f"{folder_path}/{i}" for i in file_names]
            if path is False :
                return file_names
            
        else:
            print(f"The provided path : [{folder_path}] was not found")
            return None
        
    else:

        if os.path.exists(path = folder_path):
            file_names = os.listdir(path = folder_path)

            if path: 
                return [f"{folder_path}/{i}" for i in file_names if target in i]
            if path is False:
                return [i for i in file_names if target in i]
            
        else:
            print(f"The provided path : [{folder_path}] was not found")
            return None
        

        



# print(list_dir(folder_path=r"C:\Users\Vaibhav\Desktop" , path = True))






