"""
Shortest Job First scheduler simulation.

Usage: python sjf.py [input_file]

Input format (job.txt): alternating lines <job name> / <burst time in ms>
Assumptions: all jobs arrive at time 0. Jobs run in ascending burst order.
Ties are broken by file order.
Output: schedule table, Gantt chart, per-job turnaround times, and the
average turnaround time.
"""
import sys


def read_jobs(path):
    """Return a list of (name, burst) pairs read from the input file."""
    with open(path) as f:
        tokens = [line.strip() for line in f if line.strip()]
    return [(tokens[i], int(tokens[i + 1])) for i in range(0, len(tokens) - 1, 2)]


def sjf(jobs):
    """Run jobs shortest first. Returns (schedule, turnaround dict in file order)."""
    order = sorted(jobs, key=lambda j: j[1])
    time, schedule, done = 0, [], {}
    for name, burst in order:
        start = time
        time += burst
        schedule.append((name, start, time))
        done[name] = time
    turnaround = {name: done[name] for name, _ in jobs}   # report in file order
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
    print(f"{'Job':<8}{'Start':>7}{'Stop':>7}")
    for name, s, e in schedule:
        print(f"{name:<8}{s:>7}{e:>7}")
    print("\nGantt chart:")
    print_gantt(schedule)
    print("\nTurnaround times:")
    for name, t in turnaround.items():
        print(f"  {name:<8}{t}")
    avg = sum(turnaround.values()) / len(turnaround)
    print(f"\nAverage turnaround time = {avg:.2f} ms")
    return avg


if __name__ == "__main__":
    path = sys.argv[1]
    schedule, turnaround = sjf(read_jobs(path))
    print_results(schedule, turnaround, "SJF")