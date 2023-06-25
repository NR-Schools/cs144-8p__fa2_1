from tkinter import *
from objects.process import Process
from objects.queue import Queue


class Simulator:
    def __init__(self) -> None:
        self.window = Tk("Simulation")
        self._init_ui()
        self._init_logic()

    def _init_ui(self):
        # Setup UI
        self.time_ui = Label(self.window, text="??")
        self.time_ui.pack()

        # Setup Buttons
        self.canvas = Canvas(self.window, width=800, height=600)
        self.canvas.configure(width=700, height=400, bg="#d1d1d1")
        self.canvas.pack()

        # Setup Actions
        setup = Button(self.window, text='Setup', width=20, height=1, command=self.setup)
        setup.pack()
        run_once = Button(self.window, text='Run (Once)', width=20, height=1, command=self.run_once)
        run_once.pack()

    def _init_logic(self):
        self.time = -1
        self.ready_queue: list[Process] = []
        self.executing_queue: list[Process] = []

        self.proc_data_ls: list[Process] = []

    def start_simulator(self):
        self.window.mainloop()


    def proc_list(self):
        p1 = Process([30, 30], 15).create_ui(self.canvas, "#0000FF").set_label("P1").set_logic(burst_time=4, arrival_time=0).set_visible(True)
        p2 = Process([30, 30], 15).create_ui(self.canvas, "#0000FF").set_label("P2").set_logic(burst_time=3, arrival_time=0).set_visible(True)
        p3 = Process([30, 30], 15).create_ui(self.canvas, "#0000FF").set_label("P3").set_logic(burst_time=7, arrival_time=0).set_visible(True)

        self.proc_data_ls.append(p1)
        self.proc_data_ls.append(p2)
        self.proc_data_ls.append(p3)

    def setup(self):
        # Clear Processes
        while len(self.proc_data_ls) > 0:
            self.proc_data_ls.pop().delete()
        while len(self.ready_queue) > 0:
            self.ready_queue.pop().delete()
        while len(self.executing_queue) > 0:
            self.executing_queue.pop().delete()
        
        self.proc_data_ls = []

        # Add Proc List
        self.proc_list()

        # Show Queues
        ready_queue_ui = Queue([350, 150], [300, 30]).create_ui(self.canvas, "#ff0000")
        executing_queue_ui = Queue([350, 250], [40, 30]).create_ui(self.canvas, "#00ff00")
        # 80-600; 40

    def run_once(self):
        self.proc_sched_algo(self)
    
    def set_custom_proc_sched(self, proc_sched_algo):
        self.proc_sched_algo = proc_sched_algo
    
    def adjust_ready_queue_ui(self):
        for (ind, ready_proc) in enumerate(self.ready_queue):
            x_pos = 600 - 40 * ind
            ready_proc.move([x_pos, 130])

    def log_data(self, data):
        row_str = ""
        for item in data:
            row_str += str(item).ljust(20)
        print(row_str)

    #log_data(["Process", "Remaining Time", "Time"])
    #log_data(["P1", "Finished", "4"])
    #log_data(["P2", "12", "16"])

