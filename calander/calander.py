import keyboard

def determine_month():
    valid = False
    while valid != True:
        try:
            month = int(input("Enter month (1-12):"))
            if month < 1 or month > 12:
                print("Invalid input, please enter a number between 1 and 12")
            else:
                valid = True
                return month
        except ValueError:
            print("Invalid input, please enter a number greater than 1752")

def determine_year():
    valid = False
    while valid != True:
        try:
            year = int(input("Enter year, after 1752: "))
            if year < 1753:
                print("Invalid input, please enter a number greater that 1752")
            else:
                valid = True
                return year
        except ValueError:
            print("Invalid input, please enter a number greater than 1752")
    

def compute_offset(month, year):
    total_days = 0
    for y in range(1753, year):
        if calculate_leap_year(y):
            total_days += 366
        else:
            total_days += 365
    for m in range(1, month):
        total_days += days_in_month(year, m)
    offset = (total_days + 1) % 7
    return offset
    

def display(month, year):
    print()
    print("Sun Mon Tue Wed Thu Fri Sat")

    offset = compute_offset(month, year)
    num_days = days_in_month(year, month)
    display_table(num_days, offset)

def display_table(num_days, offset):

    print("    " * offset, end="")

    for day in range(1, num_days + 1):
        print(f"{day: 3}", end=" ")
        offset += 1
        if offset % 7 == 0:
            print()
    print()
    print()

def days_in_month(year, m):
    if m == 2:
        if calculate_leap_year(year):
            num_month_days = 29
        else:
            num_month_days = 28
    elif m in [4, 6, 9, 11]:
        num_month_days = 30
    else:
        num_month_days = 31
    return num_month_days

def calculate_leap_year(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    else:
        return False

def main():

    print("press 'q' to quit.'")
    while True:
        if keyboard.is_pressed('q'):
            break
        month = determine_month()
        year = determine_year()
        display(month, year)
        
main()
