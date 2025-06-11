def fibbonacci(number, x):
    x = 0
    if number == 0:
        return 0
    if number == 1:
        return 1
    return fibbonacci(number - 1, x += 1) + fibbonacci(number - 2, x +=1)

def fibbonacci_loop(number):
    x = 0
    numbers = [0, 1]
    for i in range(number):
        numbers[i % 2] = numbers[0] + numbers[1]
        x += 1
    return numbers[number % 2], x

def main():
    number1, x = fibbonacci(20, x)
    number2, y = fibbonacci_loop(20)
    print(f"for 20 {number1} took {x} iterations")

main()