from tkinter import *
from .base_object import BaseObject

class Queue(BaseObject):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, size)
    
    def create_ui(self, canvas, color):
        self.canvas = canvas

        # Calculate Positions
        p1, p2 = self._get_points(self.pos, self.size)
        image = canvas.create_rectangle(*p1, *p2, outline=color, width=2)

        return self