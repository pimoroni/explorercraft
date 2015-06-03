import explorerhat
import explorercraft
import time

MAX_TEMP = 30
HEIGHT   = 30

thermometer = explorercraft.Thermometer(50,20,0,HEIGHT,MAX_TEMP,explorercraft.WOOL_PURPLE)
thermometer.teleport_player()

while True:
    temperature = 25 + (explorerhat.analog.one.read() - 0.75) * 100
    analog = explorerhat.analog.two.read() * (MAX_TEMP / 5.0)
    print("The temperature is {}c".format(analog))
    thermometer.update(analog)
    time.sleep(0.1)
