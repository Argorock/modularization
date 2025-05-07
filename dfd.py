def main():
    password = input("Enter Password: ")
    compare = compare_password(password)
    display(compare)

def compare_password(password):
    if password == "42":
        return True
    else:
        return False
def display(bool):
    print(bool)
main()