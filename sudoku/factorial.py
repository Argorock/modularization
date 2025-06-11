


def calculate_factorial_by_loop(n):
    factorial = 1

    for i in range(1, n+1):
        factorial *= i

    return factorial

def calculate_factorial_via_recursion(n):
    if n == 1:
        return n
    else:
        return n * calculate_factorial_via_recursion(n-1)

def main():
    print(calculate_factorial_by_loop(10))
    print(calculate_factorial_via_recursion(10))

main()