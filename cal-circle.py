import math

def calculate_circle_area(radius):
    return math.pi * radius * radius

def get_radius():
    radius = float(input("Input a radius: "))
    return radius

def main():
    radius = get_radius()
    print(calculate_circle_area(radius))

main()