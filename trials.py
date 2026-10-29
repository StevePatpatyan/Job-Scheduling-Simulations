"""
Part 3 experiment

Usage: python trials.py
 
Generates 20 random job sets for each size n which is 5, 10, 15. Burst times are
random integers between 1 and 30 and seed 17. Stores each set in
data/nXX_tYY.txt in the job.txt format and runs the same files through FCFS, SJF,
RR-2 and RR-5 and prints the average over 20 trials of the average
turnaround times for each algorithm and input size.
"""
import os, random
import fcfs, sjf, rr2, rr5
 
SIZES, TRIALS, MAX_BURST, SEED = [5, 10, 15], 20, 30, 17
ALGOS = {
    "FCFS": lambda jobs: fcfs.fcfs(jobs)[1],
    "SJF":  lambda jobs: sjf.sjf(jobs)[1],
    "RR-2": lambda jobs: rr2.round_robin(jobs)[1],
    "RR-5": lambda jobs: rr5.round_robin(jobs)[1],
}
 
 
def generate_inputs():
    """Write the 60 input files (20 trials of 3 sizes) to data/."""
    random.seed(SEED)
    os.makedirs("data", exist_ok=True)
    for n in SIZES:
        for t in range(1, TRIALS + 1):
            with open(f"data/n{n:02d}_t{t:02d}.txt", "w") as f:
                for j in range(1, n + 1):
                    f.write(f"Job{j}\n{random.randint(1, MAX_BURST)}\n")
 
 
def main():
    generate_inputs()
    print(f"{'Input size':<12}" + "".join(f"{a:>10}" for a in ALGOS))
    for n in SIZES:
        totals = {a: 0.0 for a in ALGOS}
        for t in range(1, TRIALS + 1):
            jobs = fcfs.read_jobs(f"data/n{n:02d}_t{t:02d}.txt")
            for a, run in ALGOS.items():
                totals[a] += sum(run(jobs).values()) / n    # this trial's average
        print(f"{str(n) + ' jobs':<12}" + "".join(f"{totals[a] / TRIALS:>10.2f}" for a in ALGOS))
 
 
if __name__ == "__main__":
    main()