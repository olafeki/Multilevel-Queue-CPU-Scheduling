import RR, SRT, SJF
import copy
from pandas import DataFrame
QUANTUM_RR = 3
QUANTUM_SRT = 2

# processes = []

# # get process detail as input
# n = int(input("Enter the number of processes: "))

# print("Enter the details of the processes:")
# for i in range(n):
#     print(f"\nProcess {i}: ")
#     arrival_time = int(input("Enter the arrival time: "))
#     burst_time = int(input("Enter the burst time: "))
#     priority = int(input("Enter the priority: "))
#     processes.append({'id':i, 'arrival':arrival_time,'burst':burst_time, 'priority':priority})  # [id, arrival_time, burst_time]



# processes = [
#     {'id':0, 'arrival':0, 'burst':5, 'priority':1},
#     {'id':1, 'arrival':1, 'burst':8, 'priority':0},
#     {'id':2, 'arrival':3, 'burst':6, 'priority':2},
#     {'id':3, 'arrival':5, 'burst':4, 'priority':2},
#     {'id':4, 'arrival':8, 'burst':2, 'priority':1},
#     {'id':5, 'arrival':16, 'burst':10, 'priority':0}
# ]

# processes = [
#     {'id':0, 'arrival':0, 'burst':2, 'priority':0},
#     {'id':1, 'arrival':1, 'burst':7, 'priority':1},
#     {'id':2, 'arrival':3, 'burst':5, 'priority':2},
#     {'id':3, 'arrival':3, 'burst':6, 'priority':0},
#     {'id':4, 'arrival':5, 'burst':3, 'priority':1},
# ]

processes = [
    {'id':0, 'arrival':0, 'burst':5, 'priority':2},
    {'id':1, 'arrival':0, 'burst':3, 'priority':1},
    {'id':2, 'arrival':0, 'burst':1, 'priority':0},
    {'id':3, 'arrival':10, 'burst':6, 'priority':1},
    {'id':4, 'arrival':12, 'burst':8, 'priority':2},
    {'id':5, 'arrival':14, 'burst':5, 'priority':0},
    {'id':6, 'arrival':15, 'burst':2, 'priority':0},
    {'id':7, 'arrival':17, 'burst':1, 'priority':1},
    {'id':8, 'arrival':20, 'burst':7, 'priority':2}
]

processes.sort(key=lambda x: x['arrival'])

end_time = 0
for p in processes:
    end_time = end_time + p['burst']

# gdwal fadi ll waiting time isa..
waiting_time = []
for p in processes:
    waiting_time.append({'id': p['id'], 'turnaround':0, 'waiting':0 })

high_queue = []
mid_queue = []
low_queue = []

high_ready_queue = []
mid_ready_queue = []
low_ready_queue = []
kernel_time = []

time = 0

# function to format processes and add them to list
def add_to_queue(p):
    # switch statement
    match p['priority']:
        case 0:
            high_queue.insert(0, [p['id'], p['arrival'], p['burst'], 0, p['burst']]) 
            # insert 0 34an a7otaha fl awel m4 fl a5er 34an rr 4a8al fifo??
        case 1:
            mid_queue.append([p['id'], p['burst'], p['arrival'], p['burst']])
            # zawedt burst tani 34an atra7o 34an ana batra7 mn el burst eli bab3ato fl function 34an ana habla
        case 2:
            low_queue.append([p['id'], p['arrival'], p['burst'], 0, 0]) # 0 w 0 dol waiting w turnaround
            # zawedt burst hena bardo


def update_queues():
    # loop over processes and add them to queue if they have arrived
    # ba3mel copy mn el list 34an lma ba loop over list w f nos el loop a4il menha 7aga el python by5araf ??
    # m3raf4 leh bs kan bynot tani element fl list dyman
    for p in copy.deepcopy(processes):
        if(p['arrival'] <= time):
            add_to_queue(p)
            processes.remove(p)


# ya3ni lw ay wa7da f dol fihom processes..
while(processes or high_queue or mid_queue or low_queue and time <= end_time):

    update_queues()

    print(high_queue)

    if high_queue:
        # 4a8al round robin 3al high queue

        print()
        print('RR for High Queue')

        # el round robin mal3ebte4 fiha.. sybaha bl loops b kol 7aga w m4 ha5aliha traga3li high queue
        # 34an di a3la priority fihom fa keda keda lazem t5o4 t5alas kol eli fl high queue
        # wl sara7a ana m4 adra afham code ola
        scheduler = RR.ProcessScheduler(high_queue)
        high_queue, time, high_ready_queue = scheduler.run_scheduler(time_quantum=QUANTUM_RR, start_time=time,
                                    waiting_table = waiting_time, rqueue = high_ready_queue, kernel_time = kernel_time)
        # scheduler.print_ready_queue()
        # scheduler.print_schedule(scheduler.calculate_turnaround_time(), scheduler.calculate_waiting_time(),
        # scheduler.completed_processes)
        # high_queue.clear()


    elif mid_queue:
        # 4a8al srt 3al mid queue
        for p in mid_queue:
            mid_ready_queue.append(p[0])
        print()
        print('SRT for Mid Queue')
        time, mid_queue = SRT.findWaitingTime(processes=mid_queue, n=len(mid_queue), quantum_time=QUANTUM_SRT,
                                            start_time=time, waiting_table = waiting_time, kernel_time = kernel_time)

    elif low_queue:
        # 4a8al sjf 3al low queue
        for p in low_queue:
            low_ready_queue.append(p[0])
        print()
        print('SJF for Low Queue')
        time, low_queue = SJF.shortest_job_first(processes=low_queue, start_time=time, waiting_table = waiting_time,
                                                kernel_time = kernel_time)

    else:
        time = time + 1
    
    print(kernel_time)

print()
print('end time: ', time)
print(high_queue)
print(mid_queue)
print(low_queue)
print()
print(DataFrame(waiting_time))

total_wt = 0
for i in range(len(waiting_time)):
    total_wt += waiting_time[i]['waiting']

avg = total_wt / len(waiting_time)
print("\nAverage waiting time = %.5f" % (avg))



#### GUI #####

import tkinter as tk

def create_horizontal_grid(array, row, color):
    num_items = len(array)

    for i in range(num_items):
        main_window.columnconfigure(i, weight=1, minsize=50)

        frame = tk.Frame(
            master=main_window,
            relief=tk.RAISED,
            borderwidth=1,
            bg=color
        )
        frame.grid(row=row, column=1+i, padx=5, pady=5)
        label = tk.Label(master=frame, text=f"{array[i]}", font=("Arial", 12), bg=color)
        label.pack(padx=2, pady=2)
        
def switch_lists(list1, list2):
    for item1, item2 in zip(list1, list2):
        yield item1
        yield item2

def create_alternating_grid(list1, list2, row, color1, color2):
    items_generator = switch_lists(list1, list2)

    for i, item in enumerate(items_generator):
        main_window.columnconfigure(i, weight=1, minsize=75)

        frame = tk.Frame(
            master=main_window,
            relief=tk.FLAT if i % 2 == 0 else tk.SUNKEN ,
            borderwidth=.2 if i % 2 == 0 else 1,
            bg=color1 if i % 2 == 0 else color2,
        )
        frame.grid(row=row+1 if i % 2 == 0 else row, column=i+1, padx=2, pady=2)
        label = tk.Label(master=frame, text=f"{item}", font=("Arial", 12), bg=color1 if i % 2 == 0 else color2)
        label.pack(padx=5, pady=5)
        
# Create the main window        
main_window = tk.Tk()

array1 = ["Item 1", "Item 2", "Item 3", "Item 4"]
rr = tk.Label(main_window, text="Round Robin Ready Queue:", font=("Arial", 14, "bold"))
rr.grid(row=0, column=0, pady=5, sticky='w')
create_horizontal_grid(high_ready_queue, row=0, color="lightpink2")

array2 = ["A", "B", "C", "D","E","F"]
srt = tk.Label(main_window, text="Shortest Remaining Time Ready Queue:", font=("Arial", 14, "bold"))
srt.grid(row=3, column=0, pady=5, sticky='w')
create_horizontal_grid(mid_ready_queue, row=3, color="lightpink2")

array3 = ["X", "Y", "Z"]
sjf = tk.Label(main_window, text="Shortest Job First Ready Queue:", font=("Arial", 14, "bold"))
sjf.grid(row=5, column=0, pady=5, sticky='w')
create_horizontal_grid(low_ready_queue, row=5, color="lightpink2")

emptyrow = tk.Label(main_window)
emptyrow.grid(row=8, column=0, pady=5, sticky='w')

# Example Kernel
time = []
kernel = []

for i in range(len(kernel_time)):
    p = kernel_time[i]
    if(i+1 <len(kernel_time)):
        p_next = kernel_time[i+1]
    else:
        p_next = None

    kernel.append(p['process'])
    
    # if(p_next and (p['end'] == p_next['start'])):
    #     time.append(kernel_time[i]['start'])
    # else:
    #     time.append(p['start'])
    #     time.append(p['end'])
    
    time.append(p['start'])



grand = tk.Label(main_window, text="Kernel Queue:", font=("Arial", 20, "bold italic"),fg="lightcyan4")
grand.grid(row=10, column=0, pady=5, sticky='w')
for i in range(0, len(kernel), 7):    
    create_alternating_grid(time[i:i+7], kernel[i:i+7], row= 10+i, color1="antiquewhite1", color2="lightcyan3")

main_window.mainloop()