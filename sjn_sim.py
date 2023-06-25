import pandas as pd
from simulator import Simulator
import os
from objects.process import Process

def hardcoded_res(time):
    table = None

    if time == 0:
        table = [
            [0, 4, 0, 0, 0],
            [0, 3, 0, 0, 0],
            [0, 7, 0, 0, 0]
            ]
    
    if time == 3:
        table = [
            [0, 4, 0, 0, 3],
            [0, 3, 3, 3, 0],
            [0, 7, 0, 0, 0]
            ]
    
    if time == 7:
        table = [
            [0, 4, 7, 7, 3],
            [0, 3, 3, 3, 0],
            [0, 7, 0, 0, 7]
            ]
    
    if time == 14:
        table = [
            [0, 4, 7, 7, 3],
            [0, 3, 3, 3, 0],
            [0, 7, 14, 14, 7]
            ]
    
    if table is not None:
        os.system("cls")
        df = pd.DataFrame(
            table,
            columns = ["Arrival Time", "Burst Time", "Finish Time", "Turnaround Time", "Waiting Time"],
            index=["P1", "P2", "P3"]
        )
        print(df)

def calc_min_burst_time_from_ls(proc_list: list[Process]):
    min_ind = 0
    for ind, proc in enumerate(proc_list):
        if proc.burst_time < proc_list[min_ind].burst_time:
            min_ind = ind
    
    return min_ind

def proc_sched_algo(self: Simulator):
    # Update Time
    self.time += 1
    try:
        self.time_ui['text'] = 'Time: ' + str(self.time)
    except Exception:
        pass

    hardcoded_res(self.time)
    # Update Processes

    # # Check for Arrivals
    is_proc_in_rq = False

    if len(self.proc_data_ls) > 0:

        if len(self.ready_queue) > 0:
            is_proc_in_rq = True

        curr_ind = 0
        while True:
            max_ind = len(self.proc_data_ls) -1
            if curr_ind > max_ind:
                break
            
            if self.proc_data_ls[curr_ind].arrival_time <= self.time:
                curr_ind = calc_min_burst_time_from_ls(self.proc_data_ls)
                proc = self.proc_data_ls.pop(curr_ind)
                self.ready_queue.append(proc)

                # Kung mali dis, please remove this code block
                # Check If Can Push in Executing Queue
                #if len(self.executing_queue) == 0:
                #    e_proc = self.ready_queue.pop()
                #    self.executing_queue.append(e_proc)
                #    e_proc.move([330, 225])

                # Update Positions in Ready Queue
                self.adjust_ready_queue_ui()
            else:
                curr_ind += 1

            if len(self.proc_data_ls) == 0:
                break

            if len(self.proc_data_ls) < 0 and len(self.proc_data_ls) >= curr_ind:
                break
        if is_proc_in_rq == False:
            return

    # If no more executing, push from ready_queue
    if len(self.executing_queue) == 0:
        if len(self.ready_queue) == 0:
            # No more execution
            return
        new_proc = self.ready_queue.pop(0)
        self.executing_queue.append(new_proc)
        new_proc.move([330, 225])

        # Update Positions in Ready Queue
        self.adjust_ready_queue_ui()

    # Update Executing Queue
    if len(self.executing_queue) > 0:
        curr_ind = 0
        while True:

            # # Update curr_burst_time
            self.executing_queue[curr_ind].curr_burst_time -= 1

            # # Check if process is finished
            if self.executing_queue[curr_ind].curr_burst_time <= 0:
                self.executing_queue.pop(curr_ind).delete()

                # Move New Process
                if len(self.ready_queue) == 0:
                    # No more execution
                    return
                new_proc = self.ready_queue.pop(0)
                self.executing_queue.append(new_proc)
                new_proc.move([330, 225])

            # Since Queue is supposed to be only 1
            break


s = Simulator("Shortest Job Next")
s.set_custom_proc_sched(proc_sched_algo)
s.setup()
s.run_once()
s.start_simulator()