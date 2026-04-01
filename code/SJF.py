processes = [
    {"id": "P1", "arrival": 0, "burst": 5},
    {"id": "P2", "arrival": 1, "burst": 3},
    {"id": "P3", "arrival": 2, "burst": 8},
    {"id": "P4", "arrival": 3, "burst": 6},
]

time = 0
completed = []
n = len(processes)

gantt = []  # store execution order

while len(completed) < n:
    available = [p for p in processes if p["arrival"] <= time and "done" not in p]

    if not available:
        time += 1
        continue

    shortest = min(available, key=lambda x: x["burst"])

    start = time
    time += shortest["burst"]
    end = time

    shortest["done"] = True
    shortest["start"] = start
    shortest["end"] = end

    gantt.append((shortest["id"], start, end))
    completed.append(shortest)

print("\nGantt Chart:")

for p in gantt:
    print(p[1], end="   ")
print(gantt[-1][2])

for p in gantt:
    print(f"| {p[0]} ", end="")
print("|")

print("\nProcess Table:")
print("ID  WT  TAT  RT")

total_wt = total_tat = total_rt = 0

for p in completed:
    tat = p["end"] - p["arrival"]
    wt = tat - p["burst"]
    rt = p["start"] - p["arrival"]

    total_wt += wt
    total_tat += tat
    total_rt += rt

    print(f"{p['id']}  {wt}   {tat}   {rt}")

print("\nAverage WT:", total_wt / n)
print("Average TAT:", total_tat / n)
print("Average RT:", total_rt / n)