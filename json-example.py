import json
my_data = {
    "Numbers" : [12, 234, 65, 99, 77, 12],
    "Names" : ["Bob", "Alice", "Charlie", "David", "Eve"],
    "PhoneNumbers" : ["123-456-7890", "987-654-3210", "555-555-5555", "444-444-4444", "333-333-3333"],
}

def read_data_from_json_file(file_name):
    with open(file_name, 'rt') as file_handle:
        data = file_handle.read()
        json_data = json.loads(data)
        return json_data

def write_data_to_json_file(file_name, data):
    with open(file_name, 'wt') as file_handle:
        json_data = json.dumps(data)
        file_handle.write(json_data)


def main():
    print(my_data["Numbers"])
    print(my_data["Names"]) 
    print(my_data["PhoneNumbers"])
    print(my_data)
    file_name = "my_data.json"
    write_data_to_json_file(file_name, my_data)
    new_data = read_data_from_json_file(file_name)
    print(new_data)

main()