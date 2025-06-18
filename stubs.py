

def get_int():
    # will prompt the user for an integer
    number = -1
    while number < 0:
        try:
            number = int(input("Input a positive Integer: "))
            if number < 0:
                raise TypeError
        except (ValueError, TypeError, KeyboardInterrupt):
            print("Invalid Input: Plase input a positive number: ")
    return number
        
            

def convert(number):
    # calls each calculation and passes number to be calculated
    binary = calc_bin(number)
    octal = calc_oct(number)
    hex = calc_hex(number)

    return binary, octal, hex

def calc_bin(number):
    # convert number to binary
    binary_digits = []
    binary_string = ""
    if number == 0:
        return "0"
    while number > 0:
        binary_digits.append(number % 2)
        number = number // 2

    for i in range(len(binary_digits)-1, -1, -1):
        binary_string = binary_string + str(binary_digits[i])
    return f"0b{binary_string}"

def calc_oct(number):
    # convert number to octal
    octal_digits = []
    octal_string = ""
    if number == 0:
        return "0"
    while number > 0:
        octal_digits.append(number % 8)
        number = number // 8

    for i in range(len(octal_digits)-1, -1, -1):
        octal_string = octal_string + str(octal_digits[i])
    return f"0o{octal_string}"

def calc_hex(number):
    #convert number to hex
    hex_digits = []
    hex_string = ""
    if number == 0:
        return "0"
    while number > 0:
        hex_digits.append(number % 16)
        number = number // 16
        
    hex_letters = ["A", "B", "C", "D", "E", "F"]

    for i in range(len(hex_digits)-1, -1, -1):
        if hex_digits[i] >= 10:
            letter_index = hex_digits[i] - 10
            hex_string += str(hex_letters[letter_index])
        else:
            letter_index = i
            hex_string += str(hex_digits[i])
    return f"0x{hex_string}"

def display(number, binary, octal, hex):
    # displays all the numbers
    assert type(number) == int
    assert type(binary) == str
    assert type(octal) == str
    assert type(hex) == str
    print(f"Decimal Number: {number}\nBinary Number: {binary}\nOctal Number {octal}\nHexadecimal Number: {hex}")

def test_convert_to_binary():
    #test will be made later
    assert calc_bin(255) == "0b11111111"
    assert calc_bin(1) == "0b1"
    assert calc_bin(53) == "0b110101"
    assert calc_bin(10) == "0b1010"
    print("All test passed")

def test_convert_to_octal():
    #test will be made later
    assert calc_oct(255) == "0o377"
    assert calc_oct(8) == "0o10"
    assert calc_oct(16) == "0o20"
    assert calc_oct(10) == "0o12"
    print("All test passed")

def main():
    # while True:
        #driver function, to rull all the code
        number = get_int()
        binary, octal, hex = convert(number)
        test_convert_to_binary()
        test_convert_to_octal()
        display(number, binary, octal, hex)

main()