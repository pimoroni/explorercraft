from mcpi import minecraft, block
import time

WOOL        = block.Block(35,0)
WOOL_ORANGE = block.Block(35,1)
WOOL_PURPLE = block.Block(35,2)
WOOL_BLUE   = block.Block(35,3)
WOOL_YELLOW = block.Block(35,4)
WOOL_GREEN  = block.Block(35,5)
WOOL_PINK   = block.Block(35,6)
WOOL_BLACK  = block.Block(35,7)
WOOL_GREY   = block.Block(35,8)
WOOL_LBLUE  = block.Block(35,9)
WOOL_INDIGO = block.Block(35,10)
WOOL_DBLUE  = block.Block(35,11)
WOOL_BROWN  = block.Block(35,12)
WOOL_DGREEN = block.Block(35,13)
WOOL_RED    = block.Block(35,14)
WOOL_BLACK  = block.Block(35,15)


class BarGraph():
    def __init__(self, x, y, z, height, max_value, block_style, mc=None):
        self.position = minecraft.Vec3(x,y,z)
        self.height = height
        self.block_style = block_style
        if not mc == None:
            self.mc = mc
        else:
            self.mc = minecraft.Minecraft.create()
        self.max_value = max_value
        
    def _scale_value(self, s_min, s_max, t_min, t_max, value):
        s_range = float(s_max - s_min)
        t_range = float(t_max - t_min)

        value -= s_min
        value /= s_range
        value *= t_range

        return value

    def _draw_bar(self, height):
        height = min(self.height,height)
        
        self.mc.setBlocks(
            self.position.x,
            self.position.y + height,
            self.position.z,
            self.position.x,
            self.position.y + self.height,
            block.AIR
            )
        self.mc.setBlocks(
            self.position.x,
            self.position.y,
            self.position.z,
            self.position.x,
            self.position.y + height,
            self.position.z,
            self.block_style
            )
        
    def update(self,value):
        value = self._scale_value(0, self.max_value, 0, self.height, value)
        self._draw_bar(int(value))
        
class Thermometer(BarGraph):
    def __init__(self, x, y, z, height, max_value, block_style, mc=None):
        BarGraph.__init__(self, x, y, z, height, max_value, block_style, mc)
        self._setup()

    def set_block_style(self, block):
        self.block_style = block

    def set_max_value(self, max_value):
        self.max_value = max_value

    def set_height(self, height):
        self.height = height

    def teleport_player(self):
        self.mc.player.setPos(self.position.x, self.position.y, self.position.z-30)


    def _setup(self):
        '''self.mc.setBlocks(
            self.position.x + 3,
            self.position.y - 255,
            self.position.z + 3,
            self.position.x - 3,
            self.position.y + 255,
            self.position.z - 30 - 3,
            block.AIR
            )'''
        
        self.mc.setBlocks(
            self.position.x - 3,
            self.position.y - 1,
            self.position.z - 3,
            self.position.x + 3,
            self.position.y - 30,
            self.position.z + 3,
            block.OBSIDIAN
            )

        # Draw a platform in the air for the player to stand on
        self.mc.setBlocks(
            self.position.x - 3,
            self.position.y - 1,
            self.position.z - 30 - 3,
            self.position.x + 3,
            self.position.y - 1,
            self.position.z - 30 + 3,
            block.WOOD_PLANKS
        )

        self.mc.setBlocks(
            self.position.x - 3,
            self.position.y,
            self.position.z - 30 - 3,
            self.position.x + 3,
            self.position.y,
            self.position.z - 30 + 3,
            block.FENCE
        )

        self.mc.setBlocks(
            self.position.x - 2,
            self.position.y,
            self.position.z - 30 - 2,
            self.position.x + 2,
            self.position.y,
            self.position.z - 30 + 2,
            block.AIR
        )
    
