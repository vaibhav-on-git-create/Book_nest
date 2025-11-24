import datetime

all_serials = "../Book_nest/system/serials.txt"

def generate_serial(num_range : int = 100000):

    data = [i.strip() for i in open(all_serials , "r").read().split(",")]

    return_num = 0
    for i in range(1,num_range+1):
        if str(i) in data:
            pass
        if str(i) not in data:
            open(all_serials , "a").write(f"{i},")
            return_num =  str(i)
            break
    return return_num

def generate_issue_id(name , grade  , sec ):
    name_len = len(name)
    name_char = [i for i in name]
    name_id = []

    for i in range(name_len):
        inter = name_char[i].lower()
        fragment = inter+str(i)+str(grade)+sec
        name_id.append(fragment)

    return "".join(name_id) + "--" + str(datetime.datetime.now()).replace(" " , "")
        
# print(generate_issue_id(name="Vaibhav Jaiswal" , grade="12" , sec="a"))

    



