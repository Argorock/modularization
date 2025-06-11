

def get_int():
    number = 10
    return number

def convert(number):
    binary = calc_bin(number)
    octal = calc_oct(number)
    hex = calc_hex(number)

    return binary, octal, hex

def calc_bin(number):
    return "0b11"

def calc_oct(number):
    return "o357"

def calc_hex(number):
    return "0Xf3"

def display(number, binary, octal, hex):
    print(number, binary, octal, hex)

def test_conversions():
    pass

def main():
    number = get_int()
    binary, octal, hex = convert(number)
    display(number, binary, octal, hex)

main()