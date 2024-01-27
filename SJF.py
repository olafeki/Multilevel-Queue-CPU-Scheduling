def get_process_input():
    name = input("Enter the process name: ")
    arrival_time = int(input("Enter the arrival time: "))
    burst_time = int(input("Enter the burst time: "))
    priority = int(input("Enter the priority: "))
    return name, arrival_time, burst_time, priority


def shortest_job_first(processes, waiting_table, kernel_time, start_time=0):  # start time wl waiting time da verina btehbed
    n = len(processes)
    mat = [[0 for j in range(5)] for i in range(n)]
    avg_wttime, avg_tatime = 0, 0

    processes.sort(key=lambda x: x[1])

    time = start_time
    completed = [False] * n
    completed_count = 0
    completed_processes = []  # New array to store completed process names

    # print("Steps:")
    # while completed_count < n:

    # ana 4elt dol mn gowa el while 34an 3yzah ye3mel lafa wa7da w yerga3 tani
    min_bt = float('inf')
    min_bt_index = -1

    for i in range(n):
        if processes[i][1] <= time and not completed[i] and processes[i][2] < min_bt:
            min_bt = processes[i][2]
            min_bt_index = i

    if min_bt_index == -1:
        time += 1
        # continue
        # 4elt continue mn hena w 7atet else 34an ana 4elt el while loop
    else:
        print(f"at t={time}: ", end="")
        for i in range(n):
            if processes[i][1] <= time and not completed[i]:
                print(f"{processes[i][0]}", end=" ")
        print()

        print()
        print(f"{processes[min_bt_index][0]} enters CPU")
        print()

        kernel_time.append({'process':f"P{processes[min_bt_index][0]}", 'start':time, 'end':(time+processes[min_bt_index][2])})

        time += processes[min_bt_index][2]

        processes[min_bt_index][3] = time - processes[min_bt_index][1] - processes[min_bt_index][2]
        processes[min_bt_index][4] = time - processes[min_bt_index][1]

        completed[min_bt_index] = True
        completed_count += 1
        completed_processes.append(processes[min_bt_index][0])  # Add completed process name to the list

        avg_wttime += processes[min_bt_index][3]
        avg_tatime += processes[min_bt_index][4]

        # verina btehbed
        pid = int(processes[min_bt_index][0])
        waiting_table[pid]['waiting'] = processes[min_bt_index][3]
        waiting_table[pid]['turnaround'] = processes[min_bt_index][4]

        # verina btehbed tani
        processes.remove(processes[min_bt_index])

    # avg_wttime /= n
    # avg_tatime /= n
    
    # print("\nProcess\tArrival time\tBurst time\tWaiting time\tTurnaround time")
    # for i in range(n):
    #     print(f"{processes[i][0]}\t\t{processes[i][1]}\t\t{processes[i][2]}\t\t{processes[i][3]}\t\t{processes[i][4]}")
    
    # print(f"\nThe average Waiting Time of the processes is = {avg_wttime}")
    # print(f"The average Turnaround Time of the processes is = {avg_tatime}")

    print("\nCompleted Processes:")
    for process_name in completed_processes:
        print(process_name)
    
    return time, processes
