import board
import busio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.keys import KC

from digitalio import DigitalInOut, Direction, Pull

from adafruit_mcp230xx.mcp23017 import MCP23017


i2c = busio.I2C(board.D5,board.D4,frequency = 400000)
mcp = MCP23017(i2c,adress=0x20)
NumKeys, Orientation = 61,DiodeOrientation.COL2ROW

class Scanner:
    def __init__(self,keys,cols,rows,orientation):
        self.cols = cols
        self.rows = rows
        self.orientation = True if orientation == DiodeOrientation.COL2ROW else False #True when COL2ROW and False when ROW2COL
        self.numberOfKeys = keys
        self._states = [False]*self.numberOfKeys
        self._debounce = [False]*self.numberOfKeys
        
        
        if self.orientation:
            for c in cols:
                c.direction = Direction.OUTPUT
                c.value = True
            for r in rows:
                r.direction = Direction.INPUT
                r.pull = Pull.UP
                
        else:
            for r in rows:
                r.direction = Direction.OUTPUT
                r.value = True
                
            for c in cols:
                c.direction = Direction.INPUT
                c.pull = Pull.UP
    def scan(self):
        events = []

        
        if self.orientation:
            for ci,c in enumerate(self.cols):
                c.value = False
                for ri,r in enumerate(self.rows):
                    idx = ci * len(self.rows) + ri
                    state = not r.value
                    
                    if state != self._states[idx]:
                        self._debounce[idx] += 1
                        if self._debounce[idx] >= 2:
                            self._states[idx] = state
                            self._debounce[idx] = 0
                            events.append((idx,state))
                    else:
                        self._debounce[idx] = 0
                c.value = True
        else:
            for ri,r in enumerate(self.rows):
                r.value = False
                for ci,c in enumerate(self.cols):
                    idx = ri * len(self.cols) + ci
                    state = not c.value
                    
                    if state != self._states[idx]:
                        self._debounce[idx] += 1
                        if self._debounce[idx] >= 2:
                            self._states[idx] = state
                            self._debounce[idx] = 0
                            events.append((idx,state))
                    else:
                        self._debounce[idx] = 0
                r.value = True
        return events
    
cols = [
    mcp.get_pin(3), mcp.get_pin(4), mcp.get_pin(5),    
    mcp.get_pin(8), mcp.get_pin(9), mcp.get_pin(10),   
    mcp.get_pin(11), mcp.get_pin(12), mcp.get_pin(13), 
    mcp.get_pin(14), mcp.get_pin(15),                 
    mcp.get_pin(0), mcp.get_pin(1), mcp.get_pin(2),    
]

rows = [
    DigitalInOut(board.D10),
    DigitalInOut(board.D1),
    DigitalInOut(board.D2),
    DigitalInOut(board.D3),
    DigitalInOut(board.D6)    
]

kb = KMKKeyboard()
kb.matrix = Scanner(NumKeys,cols,rows,Orientation)

#The Keymaps are AI GENEREATED, I will be changing these to a real keyboard layout that I will be using, but this is just a place holder
kb.keymap = [
    [  # Layer 0 - Standard 60% layout with extras
        # Row 0 (14 keys)
        KC.ESC,KC.N1,KC.N2,KC.N3,KC.N4,KC.N5,KC.N6,KC.N7,KC.N8,KC.N9,KC.N0,KC.MINS,KC.EQL,KC.BSPC,
        # Row 1 (14 keys)
        KC.TAB,KC.Q,KC.W,KC.E,KC.R,KC.T,KC.Y,KC.U,KC.I,KC.O,KC.P,KC.LBRC,KC.RBRC,KC.BSLS,
        # Row 2 (13 keys - 1 unused)
        KC.CAPS,KC.A,KC.S,KC.D,KC.F,KC.G,KC.H,KC.J,KC.K,KC.L,KC.SCLN,KC.QUOT,KC.ENT,KC.NO,
        # Row 3 (12 keys - 2 unused)
        KC.LSFT,KC.Z,KC.X,KC.C,KC.V,KC.B,KC.N,KC.M,KC.COMM,KC.DOT,KC.SLSH,KC.RSFT,KC.NO,KC.NO,
        # Row 4 (8 keys - 6 unused)
        KC.LCTL,KC.LGUI,KC.LALT,KC.SPC,KC.SPC,KC.RALT,KC.RCTL,KC.MO(1),KC.NO,KC.NO,KC.NO,KC.NO,KC.NO,KC.NO,
    ],
    [  # Layer 1 (Fn)
        # Row 0
        KC.GRV,KC.F1,KC.F2,KC.F3,KC.F4,KC.F5,KC.F6,KC.F7,KC.F8,KC.F9,KC.F10,KC.F11,KC.F12,KC.DEL,
        # Row 1
        KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,
        # Row 2
        KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.LEFT,KC.DOWN,KC.UP,KC.RGHT,KC.TRNS,KC.TRNS,KC.TRNS,KC.NO,
        # Row 3
        KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.NO,KC.NO,
        # Row 4
        KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.NO,KC.NO,KC.NO,KC.NO,KC.NO,KC.NO,
    ],
]