# def display_names(names):
#     for name in names:
#         print(name)

def _display_names_recursive(names):
    if not names:
        return
    else:
        print(names[0], end = " ")
        _display_names_recursive(names[1:]) # if you switch the print and call function, then it will print it in reverse order

def main():
    names = ["Adam", "Bob", "Charles", "Doug", "Eddie"]
    # display_names(names)
    _display_names_recursive(names)

main()