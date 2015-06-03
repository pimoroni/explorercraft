import explorercraft
import explorerhat
import signal

mc  = explorercraft.MinecraftInstanceHandler.Instance()

LED_OFF = explorercraft.OBSIDIAN
LED_ON  = explorercraft.GLOWING_OBSIDIAN

def red_led(x, y, z, type, face):
    explorerhat.light.red.toggle()
    if explorerhat.light.red.read():
    	mc.setBlock(x,y+1,z,LED_ON)
    else:
    	mc.setBlock(x,y+1,z,LED_OFF)

def blue_led(x, y, z, type, face):
    explorerhat.light.blue.toggle()
    if explorerhat.light.blue.read():
    	mc.setBlock(x,y+1,z,LED_ON)
    else:
    	mc.setBlock(x,y+1,z,LED_OFF)

def yellow_led(x, y, z, type, face):
    explorerhat.light.yellow.toggle()
    if explorerhat.light.yellow.read():
    	mc.setBlock(x,y+1,z,LED_ON)
    else:
    	mc.setBlock(x,y+1,z,LED_OFF)

def green_led(x, y, z, type, face):
    explorerhat.light.green.toggle()
    if explorerhat.light.green.read():
    	mc.setBlock(x,y+1,z,LED_ON)
    else:
    	mc.setBlock(x,y+1,z,LED_OFF)

mc.on_hit(handler=red_led,    block_type=explorercraft.WOOL_RED)
mc.on_hit(handler=blue_led,   block_type=explorercraft.WOOL_BLUE)
mc.on_hit(handler=yellow_led, block_type=explorercraft.WOOL_YELLOW)
mc.on_hit(handler=green_led,  block_type=explorercraft.WOOL_GREEN)

signal.pause()