# =========================================
# CPU Scheduling Simulator - FCFS Algorithm
# =========================================

class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid      # Process ID
        self.at = at        # Arrival Time
        self.bt = bt        # Burst Time
        self.ct = 0         # Completion Time
        self.tat = 0        # Turnaround Time
        self.wt = 0         # Waiting Time
        self.rt = 0         # Response Time

def fcfs(processes):
    # Sort processes by Arrival Time
    processes.sort(key=lambda x: x.at)
    
    time = 0
    gantt = []

    for p in processes:
        # CPU idle handling
        if time < p.at:
            time = p.at

        start_time = time
        p.rt = start_time - p.at

        # Execute process
        time += p.bt
        p.ct = time

        # Calculate metrics
        p.tat = p.ct - p.at
        p.wt = p.tat - p.bt

        # Add to Gantt chart
        gantt.append((p.pid, start_time, p.ct))

    return processes, gantt

# =========================================
# Function to display Gantt Chart
# =========================================
def print_gantt_chart(gantt):
    print("\nGantt Chart:")
    for p in gantt:
        print(f"| {p[0]} ", end="")
    print("|")

    # Print timeline below the chart
    for p in gantt:
        print(f"{p[1]:<4}", end="")
    print(f"{gantt[-1][2]}")

# =========================================
# Function to display process details
# =========================================
def print_process_table(processes):
    print("\nProcess Details:")
    print(f"{'PID':<5}{'AT':<5}{'BT':<5}{'CT':<5}{'TAT':<5}{'WT':<5}{'RT':<5}")
    for p in processes:
        print(f"{p.pid:<5}{p.at:<5}{p.bt:<5}{p.ct:<5}{p.tat:<5}{p.wt:<5}{p.rt:<5}")

    # Calculate and display averages
    n = len(processes)
    avg_wt = sum(p.wt for p in processes) / n
    avg_tat = sum(p.tat for p in processes) / n
    avg_rt = sum(p.rt for p in processes) / n

    print(f"\nAverage WT: {avg_wt:.2f}")
    print(f"Average TAT: {avg_tat:.2f}")
    print(f"Average RT: {avg_rt:.2f}")

# =========================================
# Main Program
# =========================================
def main():
    print("=== CPU Scheduling Simulator (FCFS) ===")

    # Option 1: Use default example
    use_default = input("Use default example processes? (y/n): ").strip().lower()
    
    if use_default == 'y':
        processes = [
            Process("P1", 0, 5),
            Process("P2", 1, 3),
            Process("P3", 2, 8),
            Process("P4", 3, 6)
        ]
    else:
        # User input
        n = int(input("Enter number of processes: "))
        processes = []
        for i in range(n):
            pid = input(f"Process {i+1} ID: ")
            at = int(input(f"Process {pid} Arrival Time: "))
            bt = int(input(f"Process {pid} Burst Time: "))
            processes.append(Process(pid, at, bt))

    # Run FCFS
    result, gantt = fcfs(processes)

    # Display outputs
    print_gantt_chart(gantt)
    print_process_table(result)

if __name__ == "__main__":
    main()