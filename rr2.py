"""
Round Robin scheduler simulation, time quantum = 2.

Usage: python rr2.py [input_file]

Input format (job.txt): alternating lines <job name> / <burst time in ms>
Assumptions: all jobs arrive at time 0 and enter the ready queue in file
order. Each turn a job runs for min(2, remaining) ms. If unfinished it goes
to the back of the queue.
Output: schedule table, each slice with its starting and stopping burst
values, Gantt chart, per-job turnaround times, and the average turnaround
time.
"""
import sys
from collections import deque

QUANTUM = 2


def read_jobs(path):
    """Return a list of (name, burst) pairs read from the input file."""
    with open(path) as f:
        tokens = [line.strip() for line in f if line.strip()]
    return [(tokens[i], int(tokens[i + 1])) for i in range(0, len(tokens) - 1, 2)]


def round_robin(jobs, q=QUANTUM):
    """Returns (schedule, turnaround dict in file order).
    schedule entries: (name, start_time, stop_time, burst_before, burst_after)."""
    remaining = {name: burst for name, burst in jobs}
    queue = deque(name for name, _ in jobs)
    time, schedule, done = 0, [], {}
    while queue:
        name = queue.popleft()
        before = remaining[name]
        run = min(q, before)
        start = time
        time += run
        remaining[name] = before - run
        schedule.append((name, start, time, before, remaining[name]))
        if remaining[name] > 0:
            queue.append(name)             # back of the line
        else:
            done[name] = time              # finished
    turnaround = {name: done[name] for name, _ in jobs}
    return schedule, turnaround

def print_gantt(segments, max_width=100):
    """Print a Gantt chart from (name, start, stop) segments. Each time label
    is placed directly under the '|' boundary it belongs to and long charts wrap to new line."""
    i = 0
    while i < len(segments):
        top, axis = "|", str(segments[i][1])
        while i < len(segments):
            name, s, e = segments[i]
            w = max(len(name), len(str(e))) + 2          # box width with padding
            if len(top) > 1 and len(top) + w + 1 > max_width:
                break                                     # wrap to a new row
            top += name.center(w) + "|"
            axis = axis.ljust(len(top) - 1) + str(e)      # label under the divider
            i += 1
        print(top)
        print(axis)

def print_results(schedule, turnaround, title):
    """
        Print results of scheduling algorithm, including Job start and stop
        times, Gantt chart, turnaround times, and ATT. The code has lots of formatting
        tricks in order to make it look good.
    """
    print(f"=== {title} ===")
    print(f"{'Job':<8}{'Start':>7}{'Stop':>7}{'Burst before':>14}{'Burst after':>13}")
    for name, s, e, b, a in schedule:
        print(f"{name:<8}{s:>7}{e:>7}{b:>14}{a:>13}")
    print("\nGantt chart:")
    print_gantt([(n, s, e) for n, s, e, _, _ in schedule])
    print("\nTurnaround times:")
    for name, t in turnaround.items():
        print(f"  {name:<8}{t}")
    avg = sum(turnaround.values()) / len(turnaround)
    print(f"\nAverage turnaround time = {avg:.2f} ms")
    return avg


if __name__ == "__main__":
    path = sys.argv[1]
    schedule, turnaround = round_robin(read_jobs(path))
    print_results(schedule, turnaround, "Round-Robin (time quantum = 2)")