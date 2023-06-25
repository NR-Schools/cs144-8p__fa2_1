from tkinter import *
from .base_object import BaseObject

class Process(BaseObject):
    def __init__(self, pos, size) -> None:
        super().__init__(pos, [size, size])
        self.is_img_created = False
        self.is_lbl_created = False

        self.is_moving = False
    
    def create_ui(self, canvas: Canvas, color):
        self.canvas = canvas

        # Calculate Positions
        p1, p2 = self._get_points(self.pos, self.size)
        self.image = canvas.create_oval(*p1, *p2, fill=color)
        self.is_img_created = True
        return self
    
    def set_label(self, text, offset=[0, 0]):
        self.label = self.canvas.create_text(self.pos[0] + offset[0], self.pos[1] + offset[1], text=text)
        self.is_lbl_created = True
        return self
    
    def set_logic(self, burst_time, arrival_time):
        self.burst_time = burst_time
        self.curr_burst_time = burst_time
        self.arrival_time = arrival_time
        return self
    
    def set_visible(self, is_visible):
        if is_visible:
            if self.is_img_created:
                self.canvas.itemconfigure(self.image, state="normal")
            if self.is_lbl_created:
                self.canvas.itemconfigure(self.label, state="normal")
        else:
            if self.is_img_created:
                self.canvas.itemconfigure(self.image, state="hidden")
            if self.is_lbl_created:
                self.canvas.itemconfigure(self.label, state="hidden")
        return self

    def move(self, new_pos, is_non_anim=False):
        self.is_moving = True

        if is_non_anim:
            self._move_ui()
        else:
            self.move_anim(new_pos)
        
        self.is_moving = False
    
    def move_anim(self, new_pos):
        move_rate = [30, 30]

        if abs(self.pos[0] - new_pos[0]) <= move_rate[0]:
            self.pos[0] = new_pos[0]
        elif self.pos[0] < new_pos[0]:
            self.pos[0] += move_rate[0]
        else:
            self.pos[0] -= move_rate[0]

        if abs(self.pos[1] - new_pos[1]) <= move_rate[1]:
            self.pos[1] = new_pos[1]
        elif self.pos[1] < new_pos[1]:
            self.pos[1] += move_rate[1]
        else:
            self.pos[1] -= move_rate[1]

        # Update object position on the canvas
        self._move_ui()

        # Check if reached destination
        if self.pos == new_pos:
            return

        # Call move_anim again after 100 milliseconds
        self.canvas.after(20, self.move_anim, new_pos)

    def _move_ui(self):
        self.canvas.moveto(self.image, self.pos[0], self.pos[1])
        self.canvas.moveto(self.label, self.pos[0]+10, self.pos[1]+10)

    def delete(self):
        if self.is_img_created:
            self.canvas.delete(self.image)
        
        if self.is_lbl_created:
            self.canvas.delete(self.label)
