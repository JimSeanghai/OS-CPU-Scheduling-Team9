def run_srt(processes):
    """
    Shortest Remaining Time (SRT) - Preemptive SJF.
    At every time unit, the process with the shortest remaining time runs.
    Returns a gantt_log: list of (pid, start, end) tuples.
    """
    import copy

    # Deep copy so original process objects are not mutated
    procs = copy.deepcopy(processes)
    n = len(procs)

    time = 0
    completed = 0
    gantt_log = []       # (pid, start_time, end_time)
    current = None       # currently running process
    current_start = None

    while completed < n:
        # Processes that have arrived and still have remaining time
        available = [p for p in procs if p.arrival_time <= time and p.remaining_time > 0]

        if not available:
            # CPU is idle — jump to the next arrival
            if current is not None:
                gantt_log.append((current.pid, current_start, time))
                current = None
                current_start = None
            next_arrival = min(p.arrival_time for p in procs if p.remaining_time > 0)
            gantt_log.append(("IDLE", time, next_arrival))
            time = next_arrival
            continue

        # Pick the process with shortest remaining time (tie-break: arrival, then pid)
        shortest = min(available, key=lambda p: (p.remaining_time, p.arrival_time, p.pid))

        # Preemption check — if a different process should run now
        if current is None or shortest.pid != current.pid:
            if current is not None:
                gantt_log.append((current.pid, current_start, time))
            current = shortest
            current_start = time

            # Record first time this process gets the CPU
            original = next(p for p in processes if p.pid == current.pid)
            if original.start_time is None:
                original.start_time = time

        # Run for 1 time unit
        current.remaining_time -= 1
        time += 1

        # Check if process just finished
        if current.remaining_time == 0:
            gantt_log.append((current.pid, current_start, time))

            original = next(p for p in processes if p.pid == current.pid)
            original.finish_time = time

            completed += 1
            current = None
            current_start = None

    return gantt_log
