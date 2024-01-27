class ProcessScheduler:
    def __init__(self, processes=[]):
        # verina btehbed
        # If process list was not given to constructor..
        # Initialize an empty list to store process details
        if processes:
            self.processes = processes
        else:
            self.processes = []
        # Initialize lists to track start time, exit time, and completed processes for Gantt chart
        self.start_time = []
        self.exit_time = []
        self.completed_processes = []
        # List to track the state of the ready queue at each time step
        self.ready_queue_states = []

    def get_process_details(self, process_id):
        # Get details for a process: arrival time and burst time
        arrival_time = float(input(f"Enter Arrival Time for Process {process_id}: "))
        burst_time = float(input(f"Enter Burst Time for Process {process_id}: "))
        return [process_id, arrival_time, burst_time, 0, burst_time]

    def get_time_quantum(self):
        # Get the time quantum from the user
        return int(input("Enter Time Quantum: "))

    def input_processes(self, num_processes):
        # Input details for each process
        for i in range(num_processes):
            process_id = int(input("Enter Process ID: "))
            process_details = self.get_process_details(process_id)
            self.processes.append(process_details)

    def run_scheduler(self, time_quantum, waiting_table, kernel_time, rqueue=[], start_time=0):
        # Initialize lists to track start time, exit time, and completed processes
        ready_queue = []
        current_time = start_time
        # verina: 4elt el sort di 34an ana dlw2ti batla3 mn el function w andaha tani ba3d kol quantum time fa da bawaz 7etet el fifo
        # # Sort processes based on arrival time
        # self.processes.sort(key=lambda x: x[1])

        #while True:
        waiting_queue = []
        current_process = []

        for i in range(len(self.processes)):
            process_id, arrival_time, burst_time, state = self.processes[i][:4]

            if arrival_time <= current_time and state == 0:
                found = 0
                if len(ready_queue) != 0:
                    for k in range(len(ready_queue)):
                        if process_id == ready_queue[k][0]:
                            found = 1
                if found == 0:
                    current_process.extend([process_id, arrival_time, burst_time, self.processes[i][4]])
                    ready_queue.append(current_process)
                    rqueue.append(current_process[0])

                    # Print process entering the ready queue
                    print(f"Time {current_time}: Process {process_id} entered the ready queue.")
                    
                    #habds
                    if(current_process[2] <= time_quantum):
                        kernel_time.append({'process':f"P{process_id}", 'start':current_time, 'end': current_time+current_process[2]})
                    else:
                        kernel_time.append({'process':f"P{process_id}", 'start':current_time, 'end': current_time+time_quantum})
                    
                    current_process = []

                if len(ready_queue) != 0 and len(self.completed_processes) != 0:
                    for k in range(len(ready_queue)):
                        if ready_queue[k][0] == self.completed_processes[-1]:
                            ready_queue.insert(len(ready_queue) - 1, ready_queue.pop(k))

            elif state == 0:
                current_process.extend([process_id, arrival_time, burst_time, self.processes[i][4]])
                waiting_queue.append(current_process)
                current_process = []

        # Store the state of the ready queue at each time step
        self.ready_queue_states.append(ready_queue.copy())

        # if len(ready_queue) == 0 and len(waiting_queue) == 0:
        #     break

        if len(ready_queue) != 0:
            r_process_id, r_burst = ready_queue[0][0], ready_queue[0][2]
            if r_burst > time_quantum:
                self.start_time.append(current_time)
                current_time += time_quantum
                end_time = current_time
                self.exit_time.append(end_time)
                self.completed_processes.append(r_process_id)

                # Print process leaving the ready queue 
                print(f"Time {current_time}: Process {r_process_id} left the ready queue.")

                for j in range(len(self.processes)):
                    c_id = self.processes[j][0]
                    if c_id == r_process_id:
                        break

                self.processes[j][2] -= time_quantum
                ready_queue.pop(0)

            elif r_burst <= time_quantum:
                self.start_time.append(current_time)
                current_time += r_burst
                end_time = current_time
                self.exit_time.append(end_time)
                self.completed_processes.append(r_process_id)

                # verina btehbed
                for j in range(len(self.processes)):
                    c_id = self.processes[j][0]
                    if c_id == r_process_id:
                        pid = j
                        break
                process = self.processes[pid]
                ta = end_time - process[1]
                wt = ta - process[4]

                waiting_table[process[0]]['waiting'] =  wt
                waiting_table[process[0]]['turnaround'] =  ta

                # Print process leaving the ready queue 
                print(f"Time {current_time}: Process {r_process_id} left the ready queue .")


                for j in range(len(self.processes)):
                    if self.processes[j][0] == ready_queue[0][0]:
                        break

                self.processes[j][2] = 0
                self.processes[j][3] = 1
                self.processes[j].append(end_time)
                ready_queue.pop(0)

        elif len(ready_queue) == 0:
            if current_time < waiting_queue[0][1]:
                current_time = waiting_queue[0][1]

            if waiting_queue[0][2] > time_quantum:
                self.start_time.append(current_time)
                current_time += time_quantum
                end_time = current_time
                self.exit_time.append(end_time)
                self.completed_processes.append(waiting_queue[0][0])

                # Print process leaving the waiting queue 
                print(f"Time {current_time}: Process {waiting_queue[0][0]} left the waiting queue .")

                for j in range(len(self.processes)):
                    if self.processes[j][0] == waiting_queue[0][0]:
                        break

                self.processes[j][2] -= time_quantum

            elif waiting_queue[0][2] <= time_quantum:
                self.start_time.append(current_time)
                current_time += waiting_queue[0][2]
                end_time = current_time
                self.exit_time.append(end_time)
                self.completed_processes.append(waiting_queue[0][0])

                # Print process leaving the waiting queue 
                print(f"Time {current_time}: Process {waiting_queue[0][0]} left the waiting queue .")

                for j in range(len(self.processes)):
                    if self.processes[j][0] == waiting_queue[0][0]:
                        break

                self.processes[j][2] = 0
                self.processes[j][3] = 1
                self.processes[j].append(end_time)

        high_queue = [x for x in self.processes if x[2] > 0]
        return high_queue, current_time, rqueue

    def calculate_turnaround_time(self):
        total_turnaround_time = 0
        for process in self.processes:
            turnaround_time = process[5] - process[1]
            total_turnaround_time += turnaround_time
            process.append(turnaround_time)

        return total_turnaround_time

    def calculate_waiting_time(self):
        total_waiting_time = 0
        for process in self.processes:
            waiting_time = process[6] - process[4]
            total_waiting_time += waiting_time
            process.append(waiting_time)

        return total_waiting_time

    def print_ready_queue(self):
        
    # Print the content of the ready queue at each time step
        for i, ready_queue_state in enumerate(self.ready_queue_states):
            if i < len(self.start_time):  # Check if the index exists in self.start_time
                 print(f"Time {self.start_time[i]}: Ready Queue - {', '.join(map(lambda x: str(x[0]), ready_queue_state))}")


    def print_schedule(self, total_turnaround_time, total_waiting_time, completed_processes):
        print("\nProcess Schedule:")
        print("Process ID\tArrival Time\tBurst Time\tCompletion Time\tTurnaround Time\tWaiting Time")
        for process in self.processes:
            print(
                f"{process[0]}\t\t{process[1]}\t\t{process[4]}\t\t{process[5]}\t\t\t{process[6]}\t\t\t{process[7]}"
            )

        print(f"\nTotal Turnaround Time: {total_turnaround_time}")
        print(f"Average Turnaround Time: {total_turnaround_time / len(self.processes)}")
        print(f"Total Waiting Time: {total_waiting_time}")
        print(f"Average Waiting Time: {total_waiting_time / len(self.processes)}")
        print(f"\nCompleted Processes: {', '.join(map(str, completed_processes))}")

    def print_gantt_chart(self):
        
        print("\nGantt Chart:")
        print("-" * 60)
        print("|", end="")

        # List to store entry and exit information
        entry_exit_info = []

        # Print the entry of the first process
        entry_exit_info.append((self.completed_processes[0], self.start_time[0], 'entered'))
       # print(f"  P{self.completed_processes[0]} entered", end="")

        for i in range(len(self.start_time)):
            print(f"  P{self.completed_processes[i]}", end="  |")

            # Add entry information
            if i + 1 < len(self.start_time):
                entry_exit_info.append((self.completed_processes[i + 1], self.exit_time[i], 'entered'))

        print("\n", "-" * 60)
        print(self.start_time[0], end="")
        # Print the entry of the first process
        print(f"  P{self.completed_processes[0]} entered", end="")
        print("\n")
        for i in range(len(self.exit_time)):
            print(f"         {self.exit_time[i]}", end="")

            # Print when a process enters the kernel
            if i + 1 < len(self.start_time):
                print(f"   P{self.completed_processes[i + 1]} entered", end="")
                entry_exit_info.append((self.completed_processes[i + 1], self.start_time[i + 1], 'entered'))

            # Add exit information
            entry_exit_info.append((self.completed_processes[i], self.exit_time[i], 'left'))

            print(f"   P{self.completed_processes[i]} left", end="")
            print()  # Add a new line after each process's entry and exit

        print()
