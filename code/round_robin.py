from collections import deque
import copy


def run_rr(processes, quantum):
    """
    Round Robin scheduling with a configurable time quantum.
    Each process gets the CPU for at most `quantum` time units before
    being preempted and moved to the back of the ready queue.
    Returns a gantt_log: list of (pid, start, end) tuples.
    """
    procs = copy.deepcopy(processes)
    n = len(procs)

    # Sort by arrival time to process arrivals in order
    procs.sort(key=lambda p: (p.arrival_time, p.pid))

    time = 0
    completed = 0
    gantt_log = []

    ready_queue = deque()   # holds process objects
    arrived_index = 0       # pointer into sorted procs list

    # Enqueue all processes that arrive at time 0
    while arrived_index < n and procs[arrived_index].arrival_time <= time:
        ready_queue.append(procs[arrived_index])
        arrived_index += 1

    while completed < n:
        if not ready_queue:
            # CPU is idle — jump to the next process arrival
            next_arrival = procs[arrived_index].arrival_time
            gantt_log.append(("IDLE", time, next_arrival))
            time = next_arrival

            while arrived_index < n and procs[arrived_index].arrival_time <= time:
                ready_queue.append(procs[arrived_index])
                arrived_index += 1
            continue

        proc = ready_queue.popleft()

        # Record first time this process gets CPU
        original = next(p for p in processes if p.pid == proc.pid)
        if original.start_time is None:
            original.start_time = time

        # How long will it actually run this slice?
        run_time = min(quantum, proc.remaining_time)
        start = time
        time += run_time
        proc.remaining_time -= run_time

        gantt_log.append((proc.pid, start, time))

        # Enqueue any new arrivals that came in during this time slice
        while arrived_index < n and procs[arrived_index].arrival_time <= time:
            ready_queue.append(procs[arrived_index])
            arrived_index += 1

        if proc.remaining_time == 0:
            # Process finished
            original.finish_time = time
            completed += 1
        else:
            # Not finished — goes back to end of ready queue
            ready_queue.append(proc)

    return gantt_log
