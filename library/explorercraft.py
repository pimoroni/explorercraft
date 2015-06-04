import mcpi.minecraft
import time
import threading
from mcpi.block import *

WOOL        = Block(35,0)
WOOL_ORANGE = Block(35,1)
WOOL_PURPLE = Block(35,2)
WOOL_BLUE   = Block(35,3)
WOOL_YELLOW = Block(35,4)
WOOL_GREEN  = Block(35,5)
WOOL_PINK   = Block(35,6)
WOOL_BLACK  = Block(35,7)
WOOL_GREY   = Block(35,8)
WOOL_LBLUE  = Block(35,9)
WOOL_INDIGO = Block(35,10)
WOOL_DBLUE  = Block(35,11)
WOOL_BROWN  = Block(35,12)
WOOL_DGREEN = Block(35,13)
WOOL_RED    = Block(35,14)
WOOL_BLACK  = Block(35,15)

BLOCK_TOP    = 1
BLOCK_BOTTOM = 0

class StoppableThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.daemon = True         

    def start(self):
        if self.isAlive() == False:
            self.stop_event.clear()
            threading.Thread.start(self)

    def stop(self):
        if self.isAlive() == True:
            self.stop_event.set()
            self.join()

class AsyncWorker(StoppableThread):
    def __init__(self, todo):
        StoppableThread.__init__(self)
        self.todo = todo

    def run(self):
        while self.stop_event.is_set() == False:
            if self.todo() == False:
                self.stop_event.set()
                break

class Singleton:
    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class MinecraftInstanceHandler(mcpi.minecraft.Minecraft):
    def __init__(self):
        mcpi.minecraft.Minecraft.__init__(self, mcpi.minecraft.Connection("localhost", 4711))
        self._hit_handlers = {}
        self._hit_polling = None

    def on_hit(self, *args, **kwargs):
        x = kwargs.get('x', -1)
        y = kwargs.get('y', -1)
        z = kwargs.get('z', -1)
        block_type = kwargs.get('block_type', Block(-1,-1))
        face    = kwargs.get('face', -1)
        handler = kwargs.get('handler', None)

        if handler == None:
            raise ValueError("Handler function required!")

        self._hit_handlers[(x, y, z, block_type, face)] = handler

        if self._hit_polling == None:
            self._hit_polling = AsyncWorker(self._poll)
            self._hit_polling.start()

    def _match_key(self, src, tgt):
        if src == tgt or src == -1 or src == Block(-1,-1):
            return True
        return False

    def _find_handlers(self, find_key):
        matching_handlers = []
        for key in self._hit_handlers:
            key_found = True
            for x in range(4):
                if not self._match_key(key[x],find_key[x]):
                    key_found = False
                    break
            if key_found and callable(self._hit_handlers[key]):
                matching_handlers.append(self._hit_handlers[key])
        return matching_handlers

    def _poll(self):
        key_all = (-1,-1,-1,Block(-1,-1),-1)
        block_hits = self.events.pollBlockHits()
        #self.events.clearAll()
        for block_hit in block_hits:
            block_type = self.getBlockWithData(block_hit.pos.x, block_hit.pos.y, block_hit.pos.z)
            key = (block_hit.pos.x, block_hit.pos.y, block_hit.pos.z, block_type, block_hit.face)

            for handler in self._find_handlers(key):
                handler(block_hit.pos.x, block_hit.pos.y, block_hit.pos.z, block_type, block_hit.face)

            '''if key in self._hit_handlers and callable(self._hit_handlers[key]):
                self._hit_handlers[key](block_hit.pos.x, block_hit.pos.y, block_hit.pos.z, block_type, block_hit.face)

            if key_all in self._hit_handlers and callable(self._hit_handlers[key_all]):
                self._hit_handlers[key_all](block_hit.pos.x, block_hit.pos.y, block_hit.pos.z, block_type, block_hit.face)'''

        time.sleep(0.01)

class ExplorercraftPlugin():
    def __init__(self,mc=None):
        if not mc == None:
            self.mc = mc
        else:
            self.mc = MinecraftInstanceHandler.Instance()

class BarGraph(ExplorercraftPlugin):
    '''Draw a bar-chart style bar with a single stack of blocks
    '''
    def __init__(self, x, y, z, height, max_value, block_style, mc=None):
        ExplorercraftPlugin.__init__(self,mc)

        self.position = mcpi.minecraft.Vec3(x,y,z)
        self.height = height
        self.block_style = block_style
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
            AIR
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
        self.mc.setBlocks(
            self.position.x - 3,
            self.position.y - 1,
            self.position.z - 3,
            self.position.x + 3,
            self.position.y - 30,
            self.position.z + 3,
            OBSIDIAN
            )

        # Draw a platform in the air for the player to stand on
        self.mc.setBlocks(
            self.position.x - 3,
            self.position.y - 1,
            self.position.z - 30 - 3,
            self.position.x + 3,
            self.position.y - 1,
            self.position.z - 30 + 3,
            WOOD_PLANKS
        )

        self.mc.setBlocks(
            self.position.x - 3,
            self.position.y,
            self.position.z - 30 - 3,
            self.position.x + 3,
            self.position.y,
            self.position.z - 30 + 3,
            FENCE
        )

        self.mc.setBlocks(
            self.position.x - 2,
            self.position.y,
            self.position.z - 30 - 2,
            self.position.x + 2,
            self.position.y,
            self.position.z - 30 + 2,
            AIR
        )
    
class Elevator(ExplorercraftPlugin):

    def __init__(self,*args,**kwargs):
        mc = kwargs.get('mc', None)
        self.x  = kwargs.get('x',0)
        self.y  = kwargs.get('y',0)
        self.z  = kwargs.get('z',0)
        self.number_of_floors = kwargs.get('number_of_floors',2)
        self.current_floor = 0

        # Height of floor from ground, including ceiling
        self.floor_height     = kwargs.get('floor_height', 3)
        ExplorercraftPlugin.__init__(self,mc)

    def _setup(self):
        total_height = self.number_of_floors * self.floor_height

        '''
        Generate the elevator shaft.
        Should be as high as the number of floors multiplied by the floor height
        But inset one step into the ground from its origin, to account for the elevator platform
        '''
        mc.setBlocks(
            self.x,self.y-1,self.z,
            self.x,self.y+total_height+1,self.z,
            AIR
        )

    def go_to_floor(self, floor):
        pass

minecraft = MinecraftInstanceHandler.Instance()