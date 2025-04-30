

def determine_K_F_C(temperature):
        if "C" in temperature.upper():
                display(temperature.upper())
                farenheit = converttoF(float(temperature[:-1]))
                kelvin = converttoK(float(temperature[:-1]))
                

        elif "F" in temperature.upper(): 
                display(temperature.upper())
                celsius = converttoC(float(temperature[:-1]))
                kelvin = converttoKfromF(float(temperature[:-1]))
                
        else:
                display(temperature.upper())
                celsius = converttoCfromK(float(temperature[:-1]))
                farenheit = converttoFfromK(float(temperature[:-1]))
                
                
def getTemperature():
        temperature = input("Enter temp farenheit (KFC): ")
        return temperature

def converttoC(farenheit):
        celsius = (farenheit - 32) * 5 / 9
        display(f"{celsius:.2f}C")

def converttoF(celsius):
        farenheit = (celsius * 9 / 5) + 32
        display(f"{farenheit:.2f}F")

def converttoK(celsius):
        kelvin = celsius + 273.15
        display(f"{kelvin:.2f}K")
        
def converttoKfromF(farenheit):
        kelvin = (farenheit - 32) * 5 / 9 + 273.15
        display(f"{kelvin:.2f}K")

def converttoCfromK(kelvin):
        celsius = kelvin - 273.15
        display(f"{celsius:.2f}C")
def converttoFfromK(kelvin):
        farenheit = (kelvin - 273.15) * 9 / 5 + 32
        display(f"{farenheit:.2f}F")

def display(temperature):
        print(temperature)

def main():
        temperature = getTemperature()
        determine_K_F_C(temperature)

main()