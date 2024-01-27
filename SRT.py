def findWaitingTime(processes, n, quantum_time, waiting_table, kernel_time, start_time=0):
    # wt da verina btehbed
    wt = [0] * n
    rt = [0] * n
    for i in range(n):
        rt[i] = processes[i][1]
    complete = 0
    t = start_time
    ready_queue = []
    execution_order = []

    # print("\nExecution Steps:")

    # 4elt el loop bardo
    # while complete != n:
    for j in range(n):
        if processes[j][2] <= t and rt[j] > 0 and j not in ready_queue:
            ready_queue.append(j)

    if not ready_queue:
        t += 1
        # continue
    else:   # bardo 4elt el continue w 7atet else
        # Find process with minimum remaining time in the ready queue
        minm = ready_queue[0]
        for j in ready_queue:
            if rt[j] < rt[minm]:
                minm = j

        print(f"at t = {t}   ", end="")
        for j in ready_queue:
            # verina: hena badal matba3 j batba3 el id bta3 j fl processes bs..
            print(f"P{processes[j][0]}  ", end="")
        print()
        # verina: hena bardo l3ebt fl print
        print(f"P{processes[minm][0]} enters the CPU")
        print()

        if(processes[minm][1] <= quantum_time):
            kernel_time.append({'process':f"P{processes[minm][0]}", 'start':t, 'end': t+processes[minm][1]})
        else:
            kernel_time.append({'process':f"P{processes[minm][0]}", 'start':t, 'end': t+quantum_time})

        if rt[minm] > quantum_time:
            t += quantum_time
            rt[minm] -= quantum_time
            processes[minm][1] -= quantum_time # verina btehbed
        else:
            t += rt[minm]
            # badelt hena 1 w 2 m4 3arfa leh bzabt
            ta = t - processes[minm][2]
            wt[minm] = ta - processes[minm][3]

            # verina btehbed
            pid = int(processes[minm][0])
            waiting_table[pid]['waiting'] =  wt[minm]
            waiting_table[pid]['turnaround'] =  ta

            rt[minm] = 0
            complete += 1
            # Print completion message after the process has completed its execution
            # verina: l3ebt fl print
            print(f"P{processes[minm][0]} leaves the CPU (Completed) at t = {t}")
            print()
            ready_queue.remove(minm)
            execution_order.append(processes[minm][0])
            processes.remove(processes[minm]) # verina btehbed

    return t, processes
    print("\nExecution queue: ", execution_order)

def findTurnAroundTime(processes, n, wt, tat):
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]

def findavgTime(processes, n, quantum_time,start_time=0):
    wt = [0] * n
    tat = [0] * n

    t = findWaitingTime(processes, n, wt, quantum_time,start_time)
    findTurnAroundTime(processes, n, wt, tat)

    print("\nProcesses    Arrival Time   Burst Time     Waiting", "Time     Turn-Around Time")
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        print(" ", processes[i][0], "\t\t", processes[i][2], "\t\t", processes[i][1], "\t\t", wt[i], "\t\t", tat[i])

    print("\nAverage waiting time = %.5f" % (total_wt / n))
    print("Average turn around time = ", total_tat / n)

    return t


