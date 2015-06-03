import explorerhat
import explorercraft
import time

MAX_TEMP = 30
HEIGHT   = 30

thermometer = explorercraft.Thermometer(0,20,0,HEIGHT,MAX_TEMP,explorercraft.WOOL_PURPLE)

thermometer.teleport_player()

potentiometer = explorercraft.BarGraph(1,20,0,50,50,explorercraft.WOOL_GREEN)

while True:
	value = max(0,min(50,int(explorerhat.analog.two.read() * 10)))
	potentiometer.update(value)

    temperature = 25 + (explorerhat.analog.one.read() - 0.75) * 100
    thermometer.update(analog)

    print("The temperature is {}c and Analog 2 is {}".format(temperature, value))

    time.sleep(0.1)
