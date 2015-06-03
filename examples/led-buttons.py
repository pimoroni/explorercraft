import explorercraft
import explorerhat
import signal

mc = explorercraft.MinecraftInstanceHandler.Instance()

def red_led(x, y, z, type, face):
    if face == explorercraft.BLOCK_TOP:
        explorerhat.light.red.toggle()

def blue_led(x, y, z, type, face):
    if face == explorercraft.BLOCK_TOP:
        explorerhat.light.blue.toggle()

def yellow_led(x, y, z, type, face):
    if face == explorercraft.BLOCK_TOP:
        explorerhat.light.yellow.toggle()

def green_led(x, y, z, type, face):
    if face == explorercraft.BLOCK_TOP:
        explorerhat.light.green.toggle()

mc.on_hit(handler=red_led,    block_type=explorercraft.WOOL_RED)
mc.on_hit(handler=blue_led,   block_type=explorercraft.WOOL_BLUE)
mc.on_hit(handler=yellow_led, block_type=explorercraft.WOOL_YELLOW)
mc.on_hit(handler=green_led,  block_type=explorercraft.WOOL_GREEN)

signal.pause()