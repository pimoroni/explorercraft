from mcpi import minecraft, block
import explorerhat
import explorercraft
import time

MAX_VALUE = 50
HEIGHT    = 50

mc = minecraft.Minecraft.create()
player = mc.player.getPos()

colours = [
    explorercraft.WOOL_GREEN,
    explorercraft.WOOL_PURPLE,
    explorercraft.WOOL_YELLOW,
    explorercraft.WOOL_RED
    ]

bars = [explorercraft.BarGraph(player.x+x,player.y,player.z+1,HEIGHT, MAX_VALUE, colours[x], mc) for x in range(4)]

while True:
    for x in range(4):
        value = min(50.0,explorerhat.analog[x].read() * 10)
        bars[x].update(value)
        print("Analog {} = {}".format(x,value))
    time.sleep(0.1)
