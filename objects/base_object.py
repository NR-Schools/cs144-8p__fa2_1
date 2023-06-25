from tkinter import *

class BaseObject:
    def __init__(self, pos, size) -> None:
        self.pos = pos
        self.size = size

    def _get_points(self, pos, size):
        p1 = [ pos[0] - size[0], pos[1] - size[1] ]
        p2 = [ pos[0] + size[0], pos[1] + size[1] ]
        return p1, p2