

def get_int():
    # will prompt the user for an integer
    number = 10
    return number

def convert(number):
    # calls each calculation and passes number to be calculated
    binary = calc_bin(number)
    octal = calc_oct(number)
    hex = calc_hex(number)

    return binary, octal, hex

def calc_bin(number):
    # convert number to binary
    return "0b11"

def calc_oct(number):
    # convert number to octal
    return "o357"

def calc_hex(number):
    #convert number to hex
    return "0Xf3"

def display(number, binary, octal, hex):
    # displays all the numbers
    print(number, binary, octal, hex)

def test_conversions():
    #test will be made later
    pass

def main():
    #driver function, to rull all the code
    number = get_int()
    binary, octal, hex = convert(number)
    display(number, binary, octal, hex)

main()