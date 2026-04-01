from collections import deque

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.start_time = -1
        self.completion = 0

# ===== TEACHER SAMPLE INPUT =====
processes = [
    Process("P1", 0, 5),
    Process("P2", 1, 3),
    Process("P3", 2, 8),
    Process("P4", 3, 6),
]

# ===== MLFQ CONFIG =====
Q1_QUANTUM = 2
Q2_QUANTUM = 4

# Queues
q1, q2, q3 = deque(), deque(), deque()

time = 0
completed = 0
n = len(processes)
gantt = []

processes.sort(key=lambda x: x.arrival)
i = 0  # pointer for arrivals

def add_arrivals():
    global i
    while i < n and processes[i].arrival <= time:
        q1.append(processes[i])
        i += 1

# ===== SIMULATION =====
while completed < n:
    add_arrivals()

    if not q1 and not q2 and not q3:
        gantt.append("Idle")
        time += 1
        continue

    if q1:
        p = q1.popleft()
        quantum = Q1_QUANTUM
        level = 1
    elif q2:
        p = q2.popleft()
        quantum = Q2_QUANTUM
        level = 2
    else:
        p = q3.popleft()
        quantum = p.remaining
        level = 3

    if p.start_time == -1:
        p.start_time = time

    exec_time = min(quantum, p.remaining)

    for _ in range(exec_time):
        gantt.append(p.pid)
        time += 1
        add_arrivals()

    p.remaining -= exec_time

    if p.remaining == 0:
        p.completion = time
        completed += 1
    else:
        # Demotion
        if level == 1:
            q2.append(p)
        elif level == 2:
            q3.append(p)
        else:
            q3.append(p)

# ===== OUTPUT =====
print("\nGantt Chart:")
print(" | ".join(gantt))

print("\nPID\tAT\tBT\tCT\tTAT\tWT\tRT")

total_wt = total_tat = total_rt = 0

for p in processes:
    tat = p.completion - p.arrival
    wt = tat - p.burst
    rt = p.start_time - p.arrival

    total_wt += wt
    total_tat += tat
    total_rt += rt

    print(f"{p.pid}\t{p.arrival}\t{p.burst}\t{p.completion}\t{tat}\t{wt}\t{rt}")

print("\nAverage Waiting Time =", total_wt / n)
print("Average Turnaround Time =", total_tat / n)
print("Average Response Time =", total_rt / n)