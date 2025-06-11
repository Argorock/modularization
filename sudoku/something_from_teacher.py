import math
# Check to see if a number is a prime number.

def is_number_prime(number):
    '''Return true if a number is Prime.
    Only have to test up to the square root of a number.'''
    if number <= 1:
        return False
    elif number == 2:
        return True
    else:            
        is_prime = True

        end_condition = math.ceil(math.sqrt(number))
        #print(end_condition)

        for counter in range(2, end_condition + 1, 1):
            is_prime = is_prime and number % counter != 0
    return is_prime

def test_is_number_prime():
    assert is_number_prime(2) == True
    assert is_number_prime(21) == False
    assert is_number_prime(23) == True
    assert is_number_prime(18700530018) == False
    assert is_number_prime(10000000019) == True
    assert is_number_prime(12347) == True
    assert is_number_prime(1) == False
    assert is_number_prime(0) == False
    assert is_number_prime(-1) == False
    print("All tests passed!")

def test_all_prime_numbers_under_limit(limit):
    for i in range(limit):
        if is_number_prime(i):
            print(f"{i} is Prime. ")
        # else:
            # print(f"{i} is not Prime. ")


def main():
    # number = 1
    # while number != 0:
    #     number = int(input("Enter a number to check if prime: "))
    #     if 1 <= number < 100 and number %  != 0:
    #         print(f"{number} is a prime number.")
    #     elif number == 0:
    #         print("Exiting the program.")
    #     else:
    #         print(f"{number} is not a prime number. ")
    test_is_number_prime()
    test_all_prime_numbers_under_limit(1000)
main()